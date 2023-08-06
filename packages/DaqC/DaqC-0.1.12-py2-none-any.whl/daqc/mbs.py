import struct
import socket
from settings import settings
import logging
import subprocess
from util import read_n_from_socket
from state import State


class MBS:

    def __init__(self, *args, **kwargs):
        self.remote, self.PASS = kwargs.get("ssh_target")
        self.dir = kwargs.get("directory")
        self.user = kwargs.get("user")
        self.backend_log = logging.getLogger("backend")
        self._status = MbsStatusCollector(settings['mbs']['hostname'])
        self.__stop = None

        self.mbs_version = settings['mbs']['version']
        self.mbs_bin = settings['mbs']['bin']
        self.mbs_root = settings['mbs']['root']
        self.rshell = "{}/script/rshell.sc".format(self.mbs_root)
        self.reset = "{}/m_remote reset".format(self.mbs_bin)
        self.dispatch = "{}/m_dispatch".format(self.mbs_bin)
        self.startup = settings['mbs']['startup']
        self.shutdown = settings['mbs']['shutdown']

        reset_cmd = settings['mbs']['reset']
        if reset_cmd == 'resl':
            self.reset += " -l"
        elif reset_cmd == 'resa':
            pass
        else:
            raise ValueError("Unknown reset command. Only resl and resa supported!")

    def is_running(self):
        return self._status.update()

    def start(self):
        self.backend_log.info("Started MBS")
        self.__stop = False
        self._execute_command(self.reset)
        self._execute_command("{} {} >> /dev/null".format(self.dispatch, self.startup))
        self._status.update() # Force status update, so we go into stating state
        self.backend_log.info("Started MBS - done")

    def stop(self):
        self.backend_log.info("Stopping MBS")
        self.__stop = True
        self._execute_command("{} {} >> /dev/null".format(self.dispatch, self.shutdown))
        self._execute_command(self.reset)
        self.backend_log.info("Stopping MBS - done")

    def _execute_command(self, command):
        import shlex
        cmd = "ssh {}@{} '{} {} {} {}' ".format(self.user, self.remote, self.rshell, self.mbs_version, self.dir, command)
        p = subprocess.Popen(shlex.split(cmd))
        return p.communicate()

    def status(self):
        interesting = ['bh_acqui_started', 'bh_acqui_running', 'bl_n_events',
                       'bl_n_kbyte', 'bl_n_strserv_kbytes', 'bl_r_events',
                       'bl_r_kbyte', 'bl_r_strserv_kbytes', 'bl_pipe_size_KB',
                       'bl_pipe_size_KB', 'bl_pipe_filled_KB']

        result = {}
        for i in interesting:
            result[i] = getattr(self._status, i)

        return result

    def state(self):
        # We want to stop
        if self.__stop:
            if self.is_running():
                return State.STOPPING
            else:
                return State.STOPPED
        # We should be running
        else:
            if not self.is_running():
                return State.CRASHED
            elif self._status.bh_acqui_running:
                return State.RUNNING
            else:
                return State.STARTING

    def get_name(self):
        return "MBS"
#
# This class is heavily inspired by the implementation in GSI GO4
#
class MbsStatusCollector:

    @staticmethod
    def no_op(x):
        return x

    def __init__(self, host):
        from cffi import FFI

        self.host = host
        self.log = logging.getLogger("backend")
        self.ffi = FFI()
        self.convert = MbsStatusCollector.no_op

        self.ffi.cdef("""
typedef char CHARS;
typedef int INTS4;
typedef unsigned int INTU4;
typedef struct
{
  INTU4 l_endian;               /* set to 1 if sent */
  INTU4 l_version;              /* increment in f_ut_status_ini after changes */
  INTU4 l_daqst_lw;             /* sizeof(s_daqst)/4 : number of lw */
  INTU4 l_fix_lw;               /* (&c_pname-ps_daqst)/4 : fix number of longwords to read */
  INTU4 l_sys__n_max_procs;     /* maximum number of processes */
  INTU4 l_sbs__str_len_64;      /* String length of process names */
  INTU4 l_sbs__n_trg_typ;       /* maximum number of triggers */
  INTU4 bh_daqst_initalized;    /* crea_daqst */
  INTU4 bh_acqui_started;       /* util(f_ut_op_trig_mod), read_cam_slav, read_meb */
  INTU4 bh_acqui_running;       /* collector, read_cam_slav, read_meb  */
  INTU4 l_procs_run;            /* processes running (index in l_pid) */
  INTU4 bh_setup_loaded;        /* util(f_ut_load_setup) */
  INTU4 bh_set_ml_loaded;       /* util(f_ut_load_ml_setup) */
  INTU4 bh_set_mo_loaded;       /* util(f_ut_load_mo_setup) */
  INTU4 bh_cam_tab_loaded;      /* read_cam_slav, read_meb) */
  INTS4 l_free_streams;         /* transport */
  INTU4 bl_n_events;            /* collector */
  INTU4 bl_n_buffers;           /* collector f_col_format */
  INTU4 bl_n_bufstream;         /* transport */
  INTU4 bl_n_kbyte;             /* transport */
  INTU4 bl_n_evserv_events;     /* event_serv f_ev_checkevt  */
  INTU4 bl_n_evserv_kbytes;     /* event_serv f_ev_send */
  INTU4 bl_n_strserv_bufs;      /* stream_serv  */
  INTU4 bl_n_strserv_kbytes;    /* stream_serv  */
  INTU4 bl_n_kbyte_tape;        /* transport  */
  INTU4 bl_n_kbyte_file;        /* transport  */
  INTU4 bl_r_events;            /* rate  */
  INTU4 bl_r_buffers;           /* rate  */
  INTU4 bl_r_bufstream;         /* rate  */
  INTU4 bl_r_kbyte;             /* rate  */
  INTU4 bl_r_kbyte_tape;        /* rate  (from l_block_count) */
  INTU4 bl_r_evserv_events;     /* rate  */
  INTU4 bl_r_evserv_kbytes;     /* rate  */
  INTU4 bl_r_strserv_bufs;      /* rate  */
  INTU4 bl_r_strserv_kbytes;    /* rate  */
  INTU4 bl_flush_time;          /* stream flush time */
  INTS4 l_pathnum;              /* path number of open device */
  INTU4 l_block_length;         /* current block length */
  INTU4 l_pos_on_tape;          /* current tape position in kB */
  INTU4 l_max_tape_size;        /* maximal tape length in kB */
  INTU4 l_file_count;           /* file count on volume */
  INTU4 l_file_auto;            /* file count on volume */
  INTU4 l_file_cur;             /* file count on volume */
  INTU4 l_file_size;            /* file size */
  INTU4 l_block_count;          /* buffers on file */
  INTU4 l_block_size;           /* block size (=buffer) in bytes */
  INTU4 l_record_size;          /* record size on bytes */
  INTS4 l_open_vol;             /* open mode of volume */
  INTS4 l_open_file;            /* open  file flag */
  INTS4 l_rate_on;              /* for m_daq_rate */
  INTS4 l_rate_sec;             /* for m_daq_rate */
  INTU4 bh_trig_master;         /* util(f_ut_op_trig_mod) */
  INTU4 bh_histo_enable;        /* collector */
  INTU4 bh_histo_ready;         /* collector */
  INTU4 bh_ena_evt_copy;        /* collector */
  INTU4 bl_n_trig[16];          /* Trigger counter (read_cam_slav or read_meb) */
  INTU4 bl_n_si [16];           /* Invalid subevents (collector) */
  INTU4 bl_n_evt [16];          /* Valid triggers (collector) */
  INTU4 bl_r_trig[16];          /* Rate Trigger counter (read_cam_slav or read_meb) */
  INTU4 bl_r_si [16];           /* Rate Invalid subevents (collector) */
  INTU4 bl_r_evt [16];          /* Rate Valid triggers (collector) */
  INTU4 bh_running[30];         /* run bit for tasks */
  INTU4 l_pid[30];              /* pid table */
  INTU4 l_type[30];             /* Type number defined in sys_def.h */
  INTS4 l_pprio[30];            /* daq processes priority */
  /*   f_ut_clear_daqst,    */
  /*   f_ut_exit_daq_proc,  */
  /*   f_ut_show_acq,       */
  /*   dispatch,            */
  /*   prompt               */
  /*   tasks                */
  INTU4 bh_pact[30];            /* daq processes, 1 = active, as pprio */
  INTU4 bh_verbose_flg;         /**/
  INTU4 bl_histo_port;          /* not used */
  INTU4 bl_run_time;            /* not used */
  INTS4 l_irq_driv_id;          /* 0=irq driver/device not installed */
  INTS4 l_irq_maj_dev_id;       /*            "="                    */
  INTU4 bh_event_serv_ready;    /* event_serv, stream_serv */
  INTU4 bl_strsrv_scale;        /* stream server */
  INTU4 bl_strsrv_sync;         /* stream server */
  INTU4 bl_strsrv_nosync;       /* stream server */
  INTU4 bl_strsrv_keep;         /* stream server */
  INTU4 bl_strsrv_nokeep;       /* stream server */
  INTU4 bl_strsrv_scaled;       /* stream server */
  INTU4 bl_evtsrv_scale;        /* event server */
  INTU4 bl_evtsrv_events;       /* event server */
  INTU4 bl_evtsrv_maxcli;       /* event server */
  INTU4 bl_evtsrv_all;          /* event server */
  INTU4 bl_esosrv_maxcli;       /* esone server */
  INTU4 bl_pipe_slots;          /* sub event slots in readout pipe */
  INTU4 bl_pipe_slots_filled;   /* sub event slots used */
  INTU4 bl_pipe_size_KB;        /* readout pipe size */
  INTU4 bl_pipe_filled_KB;      /* readout pipe size occupied */
  INTU4 bl_spill_on;            /* Spill on/off */
  INTU4 bl_delayed_eb_ena;      /* Delayed event building enabled/disab.*/
  INTU4 bl_event_build_on;      /* Event building on/off */
  INTU4 bl_dabc_enabled;        /* DABC event builder mode off/on */
  INTU4 bl_trans_ready;         /* transport server ready */
  INTU4 bl_trans_connected;     /* Client to transport connected */
  INTU4 bl_no_streams;          /* Number of streams */
  INTU4 bl_user[16];            /* for user */
  INTU4 bl_filler[190];         /* filler */
  INTU4 bl_no_stream_buf;       /* bufs per stream */
  INTU4 bl_rfio_connected;      /* RFIO connected */
  CHARS c_user[64];             /* username */
  CHARS c_date[64];             /* date of last update (m_daq_rate) */
  CHARS c_exprun[64];           /* run name */
  CHARS c_exper[64];            /* experiment */
  CHARS c_host[64];             /* name of host */
  CHARS c_remote[64];           /* name of remote control node */
  CHARS c_display[64];          /* name of remote display node */
  CHARS c_anal_segm_name[64];   /* name of histogram segment in use */

  /* by f_his_anal() in m_collector   */
  CHARS c_setup_name[64];       /* setup table loaded */
  CHARS c_ml_setup_name[64];    /* ml setup table loaded */
  CHARS c_readout_name[64];     /* readout table loaded */
  CHARS c_pathstr[64];          /* path string */
  CHARS c_devname[64];          /* Name of tape device */
  CHARS c_tape_label[64];       /* current tape label */
  CHARS c_file_name[256];       /* current file name */
  CHARS c_out_chan[64];         /* active ouput media */

  /* ------------------ end of fixed block --------------------------*/
  /*CHARS c_pname[30][64];*/    /* as pprio */
} s_daqst;
    """)

        self.daqst = self.ffi.new("s_daqst*")
        self.daqst_buffer = self.ffi.buffer(self.daqst)

    def update(self):
        s = None
        try:
            s = socket.socket()
            s.connect((self.host, 6008))
            s.sendall(struct.pack("!I", 1))

            # Reads l_endian, l_version, l_daqst_lw, l_fix_lw
            header_buffer = read_n_from_socket(s, 16)

            endian = '<' if struct.unpack('<I', bytes(header_buffer[0:4])) == 1 else '>'

            header = struct.unpack(endian + 'I'*4, bytes(header_buffer))
            fix_lw = header[3]  # n words until c_pname
            body_buf = read_n_from_socket(s, 4*fix_lw-16)

            self.daqst_buffer[0:16] = header_buffer
            self.daqst_buffer[16:] = body_buf

            # Read out c_pname
            remaining = socket.ntohl(self.daqst.l_sbs__str_len_64)*socket.ntohl(self.daqst.l_procs_run)
            read_n_from_socket(s, remaining)

            if self.daqst.l_endian == 1:
                self.convert = MbsStatusCollector.no_op
            else:
                self.convert = socket.ntohl

            return True

        except Exception as e:
            self.log.warning("Mbs status connect failed due to %s" % e)
            return False

        finally:
            if s is not None:
                s.close()

    def __getattr__(self, name):
        attribute = self.daqst.__getattribute__(name)
        if name.startswith('c'):
            return attribute

        number = self.convert(attribute)
        if name.startswith('bh'):
            return number > 0
        else:
            return number


class MockMBS:
    def __init__(self, **_):
        self.running = None
        self.backend_log = logging.getLogger("backend")
        self.backend_log.info("Created MockMBS")

    def stop(self):
        self.backend_log.info("Stopping MockMBS")
        self.running = False
        self.backend_log.info("Stopping MockMBS - done")

    def start(self):
        self.backend_log.info("Starting MockMBS")
        self.running = True
        self.backend_log.info("Starting MockMBS - done")

    def is_running(self):
        return self.running

    @staticmethod
    def status():
        interesting = ['bh_acqui_started', 'bh_acqui_running', 'bl_n_events',
                       'bl_n_kbyte', 'bl_n_strserv_kbytes', 'bl_r_events',
                       'bl_r_kbyte', 'bl_r_strserv_kbytes', 'bl_pipe_size_KB',
                       'bl_pipe_size_KB', 'bl_pipe_filled_KB']

        result = {}
        for i in interesting:
            result[i] = 0

        return result

    def state(self):
        if self.running is None:
            return State.STANDBY
        elif self.running:
            return State.RUNNING
        else:
            return State.STOPPED


    def get_name(self):
        return "MockMBS"