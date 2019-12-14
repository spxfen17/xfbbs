$(function () {
   $("#submit-btn").click(function (event) {
      event.preventDefault();
      var telephone_input = $("input[name='telephone']");
      var password_input = $("input[name='password']");
      var remember_input = $("input[name='remember']")

      var telephone = telephone_input.val();
      var password = password_input.val();
      var remember = remember_input.checked ? 1:0;

      zlajax.post({
          'url':'/signin/',
          'data':{
              'telephone':telephone,
              'password':password,
              'remember':remember
          },
          'success':function (data) {
              if(data['code'] == 200){
                  window.location = '/'
              }else {
                  xtalert.alertInfo(data['message'])
              }
          },
          'fail':function () {
              xtalert.alertNetworkError()
          }
      });
   });
});