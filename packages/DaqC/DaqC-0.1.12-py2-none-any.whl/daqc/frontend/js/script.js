﻿
var app = angular.module('DAQController', ['ui.bootstrap', 'blockUI', 'ngRoute', 'emguo.poller']);

var BEAM_REGEX=/([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?) *(\D+)/;

app.service('api', function($http) {

    this.get_status = function(success, error) {
        return $http.get('/api/status')
    }

    this.get_logs = function(success, error) {
        return $http.get('/api/logs')
    }

    this.start_file = function(file_size, success, error) {
        var pat = /\d+[kMG]/;
        if(!pat.test(file_size)) {
            file_size = "100M";
        }
        return $http.post('/api/start_file', JSON.stringify({size: file_size}))
    }

    this.send_info = function(data,
                                success, error) {

        if(data.beam_e) {
            var match = BEAM_REGEX.exec(data.beam_e);
            data.beam_energy = match[1];
            data.beam_energy_unit = match[2];
        }
        else {
            if ('beam_energy' in data) delete data['beam_energy']
            if ('beam_energy_unit' in data) delete data['beam_energy_unit']
        }
        var payload = JSON.stringify(data);

        return $http.post('/api/send_info', payload)
    }

    this.stop_file = function(success, error) {
        return $http.post('/api/stop_file')
    }

    this.login = function(user, pass) {
        return $http.post('/api/login', {username: user, password: pass});
    }

    this.logout = function() {
        return $http.post('/api/logout');
    }

    this.profile = function() {
        return $http.get('/api/profile')
    }

    this.trigger_names = function() {
        return $http.get('/api/trigger_names')
    }

    this.update_trigger_names = function() {
        return $http.get('/api/update_trigger_names')
    }

    this.last_info = function() {
        return $http.get('/api/last_file_info')
    }

    this.set_trigger = function(trigger, downscaling) {
        return $http.post('/api/set_trigger', {trigger: trigger, downscaling:downscaling})
    }

    this.toggle = function(service, what) {
        return $http.post('/api/toggle', JSON.stringify({who:service, what: what}))

    }
})

app.service('Session', function () {
    this.create = function (sessionId, userId, userRole) {
        this.id = sessionId;
        this.userId = userId;
        this.userRole = userRole;
  };
    this.destroy = function () {
        this.id = null;
        this.userId = null;
        this.userRole = null;
  };
})

app.directive('beamenergy', function (){
   return {
      require: 'ngModel',
      link: function(scope, elem, attr, ngModel) {

            var func = function(value) {
             var valid = !value || value=="" || BEAM_REGEX.test(value)
             ngModel.$setValidity('beamenergy', valid);
             return valid ? value : undefined;
          };
          //For DOM -> model validation
          ngModel.$parsers.unshift(func);

          //For model -> DOM validation
          ngModel.$formatters.unshift(func);
      }
   };
});

app.service('AuthService', function(api, Session) {
    this.login = function(user, pass) {
        user = user.trim();
        pass = pass.trim();

        return api.login(user, pass).then( function (res) {
            var data = res.data;
            Session.create(data.access_token, user, 'filer')
            return user;
        });
    }

    this.logout = function(user, pass) {
        return api.logout().then( function (res) {
            Session.destroy();
            return null
        });
    }

    this.is_authenticated = function() {
        return !!Session.userId
    }
});


app.controller('TabCtrl', function($scope) {
    $scope.tab=1
    $scope.f="active"
    $scope.b=$scope.s=""
});

app.controller('LogsCtrl', function($scope, poller, api) {
    $scope.tab=3
    $scope.c="active"
    $scope.a=$scope.b=""


    var p = poller.get('/api/logs',{delay:1000});
    p.promise.then(null, null, function(data) {
        $scope.synclog = data.data.synclog.reverse();
        $scope.log = data.data.log.reverse();
        $scope.datadir = data.data.data_dir;
        $scope.relay_ucesb_log = data.data.relay_ucesb_log;
        $scope.file_ucesb_log = data.data.file_ucesb_log;
        $scope.go4_log = data.data.go4_log;
    });

    $scope.$on("$destroy", function(){
        p.stop();
    });

});

app.controller('StatusController', function($scope, api, Session, blockUI, $interval, poller) {

    var block = blockUI.instances.get('total_block');

    $scope.connected = false;

    $scope.file_sizes = ['10M', '50M', '100M', '200M', '500M', '1G'];
    $scope.file_size = $scope.file_sizes[2];

    $scope.currentUser = null;
    $scope.set_current_user = function(user) {
        $scope.currentUser = user;
    }

    api.profile().success(function(data) {
        $scope.set_current_user(data.username);
    })

    $scope.toYYYYMMHHMMSS = function(date) {
        return moment(date).format("YYYY-MM-DD k:mm:ss");
    }

    $scope.toHHMMSS = function(date) {
        return moment(date).format("k:mm:ss");
    }

    var p = poller.get('/api/status',{delay:1000,catchError: true, action: 'get'});
    p.promise.then(null, null, function(response) {
        if(response.status==200) {
            data = response.data;
            $scope.readout_lib = data.readout_lib;
                $scope.vme_lib = data.vme_lib;
                $scope.relay = data.relay;
                $scope.go4 = data.go4;
                $scope.mesytec = data.mesytec;
                $scope.vme = data.vme;
                $scope.sync = data.sync;
                $scope.file = data.file;
                $scope.disk = data.disk;
                $scope.filelog = data.filelog;
                $scope.rundb = data.rundb;
                $scope.trigger = data.trigger;
                $scope.datadir = data.data_dir;

                if($scope.file.start_time) {

                    var ms = moment().diff(moment($scope.file.start_time));
                    var d = moment.duration(ms);
                    var hours = Math.floor(d.asHours());
                    if(hours<10) hours = "0" + hours;
		            $scope.file.file_length = hours + moment.utc(ms).format(":mm:ss");
		        }
                if (!$scope.connected) block.stop()

                $scope.connected = true;

        }
        else {
            if ($scope.connected) {
                block.start();
                block.message('Connection lost');
            }
            $scope.connected = false;
        }

    });
});

app.controller('ServiceController', function($scope, api, Session, blockUI) {

    var block = blockUI.instances.get('services_block');

    $scope.toggle = function(service, toggle) {
        api.toggle(service, toggle);
    }

    $scope.update_names = function() {
        api.update_trigger_names().success(function(response) {
            $scope.names = response.names;
        });
    }

    $scope.stopableState = function(state) {
        return state == "running" || state == "starting";
    }

    $scope.restartable = function(service) {
        return service == "Go4" || service == "Relay";
    }

    $scope.$watch('currentUser', function(newValue, oldValue) {
        if (!!newValue) block.stop();
        else {
            block.start();
            block.message('Please login');
        }
    });

});

var TriggerModalCtrl = function ($scope, api, $modalInstance, names, status, downscaling) {

    $scope.FOUR = [0, 1, 2, 3];
    $scope.names = names;
    $scope.selected = status;
    $scope.downscaling = downscaling;
    $scope.ok = function () {
        result = [];
        for(var i=0; i<$scope.selected.length; i++) {
            if ($scope.selected[i]) result.push(i+1);
        }
        $modalInstance.close({result:result, downscaling, downscaling});
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
};

app.controller('TriggerCtrl', function($scope, $modal,  api, Session) {

    $scope.FOUR = [0, 1, 2, 3];
    $scope.setting = false;
    $scope.Math = window.Math;

    $scope.to_exp = function(ds) {
        var r = Math.pow(2,ds);
        if(r > 1e6) return r.toExponential(1);
        return r;
    }

    api.trigger_names([]).success(function (response) {
        $scope.downscaling = response.downscaling;
        $scope.names = response.names;
    }).error(function(response) {
        alert(response.message);
    });

    $scope.open = function () {
        var modalInstance = $modal.open({
            templateUrl: 'TriggerView',
            controller: TriggerModalCtrl,
            windowClass: 'app-modal-window',
            backdrop  : 'static',
            keyboard  : false,
            resolve: {
                names: function() {return $scope.names;},
                status: function() {return $scope.trigger.status;},
                downscaling: function() {return $scope.trigger.downscaling;}
            }
        });

        modalInstance.result.then(
            function (new_trigger) {
                $scope.setting = true;
                api.set_trigger(new_trigger.result, new_trigger.downscaling).success(function (response) {
                    $scope.setting = false;
                }).error(function (response) {
                    alert(response.message);
                    $scope.setting = false;
                })
            },
            function () {
                console.log("Cancel")
            }
        );
    };
});

var ModalInstanceCtrl = function ($scope, api, $modalInstance, currentLog, logState) {

    $scope.currentLog = currentLog;
    $scope.logState = logState;
    $scope.ok = function () {
        $modalInstance.close($scope.currentLog);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
};

app.controller('LoginCtrl', function($rootScope, $scope, AuthService, $timeout) {
    $scope.login = function(credentials) {
        if (!credentials) return;

  // anything you want can go here and will safely be run on the next digest.

        AuthService.login(credentials.user, credentials.pass).then(function (user) {
            $scope.set_current_user(user);
        }, function (res) {
            $timeout(function() {
                alert("Wrong username or password");
            });
        });
    }

    $scope.logout = function(credentials) {
        AuthService.logout().then(function() {
            $scope.set_current_user(null);
        });
    }
});

app.controller('FileCtrl', function($scope, api, $http, blockUI, $modal) {
    var block = blockUI.instances.get('file_block');

    $scope.open = function () {
        api.last_info().then(function(resolve){
            $scope.currentLog = resolve.data;
            $scope.openModal()

        }, function(reject) {
            if(!$scope.currentLog) $scope.currentLog={type:'Run', facility:'IFA'};
            $scope.openModal()
        });
    }

    $scope.openModal = function() {
        var modalInstance = $modal.open({
            templateUrl: 'LogInputView',
            controller: ModalInstanceCtrl,
            backdrop  : 'static',
            keyboard  : false,
            resolve: {
                currentLog: function () {
                    if(!$scope.currentLog) $scope.currentLog={type:'Run', facility:'IFA'};
                    return $scope.currentLog;
                },
                logState: function () {
                    return $scope.logState;
                }
            }
        });

        modalInstance.result.then(function (currentLog) {

                $scope.currentLog = currentLog;
                api.send_info(currentLog)
            }, function () {
                api.send_info($scope.currentLog)
            }
        );
    };

    $scope.$watch('currentUser', function(newValue, oldValue) {
        if (!!newValue) block.stop();
        else {
            block.start();
            block.message('Please login');
        }
    });

    $scope.startFile = function() {
        if($scope.disk.message == "Not found!") {
            alert("The specified directory is not valid! We have nowhere to put the file!");
        }
        else {
            api.start_file($scope.file_size).success(function (data) {
                $scope.open();
            })
            .error(function(x) {
                alert(x.fail)
            });
        }
    };

    $scope.stopFile = function() {
        api.stop_file();
        $scope.open();
    };

    $scope.submit = function() {
        var status = $scope.file.status;
        if (status === 'running') $scope.stopFile();
        else if (status === 'stopped') $scope.startFile();
    }

});

app.config(['$routeProvider', function(routing) {
        routing
            .when('/logs', {
                templateUrl: 'partials/logs.html'
            })
            .when('/', {
                templateUrl: 'partials/home.html'
            })
            .when('/settings', {
                templateUrl: 'partials/settings.html'
            })
            .otherwise({
                redirect: '/'
            });
}]);
