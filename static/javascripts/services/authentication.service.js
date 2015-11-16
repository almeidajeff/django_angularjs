/**
* Authentication
* @namespace django_angularjs.authentication.services
*/
(function () {
  'use strict';

  angular
    .module('django_angularjs.authentication.services')

    /* Essa linha registra um factory com o nome Authentication no módulo da linha anterior. */
    .factory('Authentication', Authentication);

    /* Injetando os cookies e http no factory criado */
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

    /*  Definir o serviço como um objeto chamado e, em seguida, devolvê-lo, deixando os detalhes menores no arquivo. */
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

    /* Neste ponto, o serviço de autenticação tem apenas um método: registrar, o que leva um nome de usuário, senha e e-mail. 
    * TODO: Adicionar novos métodos aqui */
    function register(email, password, username) {
      return $http.post('/api/v1/accounts/', {
        username: username,
        password: password,
        email: email
      });
    }
  }
})();