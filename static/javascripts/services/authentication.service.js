/**
* Authentication
* @namespace django_angularjs.authentication.services
*/
(function () {
  'use strict';

  angular
    .module('django_angularjs.authentication.services')
    .factory('Authentication', Authentication);

  Authentication.$inject = ['$cookies', '$http'];

  /**
  * @namespace Authentication
  * @returns {Factory}
  */
  function Authentication($cookies, $http) {
    /**
    * @name Authentication
    * @desc The Factory to be returned
    */
    var Authentication = {
      register: register
    };

    return Authentication;

    ////////////////////

    /**
    * @name registrar
    * @desc Tenta registrar um novo usuário
    * @param {string} username, o nome de usuário digitado pelo usuário
    * @param {string} password, a senha digitada pelo usuário
    * @param {string} email, E-mail digitado pelo usuário
    * @returns {Promise}
    * @memberOf django_angularjs.authentication.services.Authentication
    */
    function register(email, password, username) {
      return $http.post('/api/v1/accounts/', {
        username: username,
        password: password,
        email: email
      });
    }
  }
})();