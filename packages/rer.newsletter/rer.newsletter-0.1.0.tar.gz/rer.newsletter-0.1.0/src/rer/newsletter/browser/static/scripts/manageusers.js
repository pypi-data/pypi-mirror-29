require.config({
    "paths": {
      "datatables": PORTAL_URL + "/++plone++rer.newsletter/scripts/datatables",
    }
});
requirejs(["jquery", "mockup-patterns-modal", "datatables"], function($, Modal, datatables){

  function render_error(message){
    $('.portalMessage').removeClass('info')
                       .addClass('error')
                       .css('display', '')
                       .html('<strong>Error</strong> ' + message);
  }

  function render_info(message){
    $('.portalMessage').removeClass('error')
                       .addClass('info')
                       .css('display', '')
                       .html('<strong>Info</strong> ' + message);
  }

  $(document).ready(function() {
    var table = null;
    // var num_users_table = 0;

    // triggero l'apertura delle modal
    $('#users-export > span').on('click', function(){
      $.ajax({
        url: "exportUsersListAsFile"
      })
      .done(function(data){
        var blob = new Blob(["\ufeff", data]);
        var url = URL.createObjectURL(blob);

        var downloadLink = document.createElement("a");
        downloadLink.href = url;
        downloadLink.download = "data.csv";

        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
      });
    });

    $('#delete-user > span').on('click', function(){
      if (!(table.row('.selected').data())){
        render_error('Prima va selezionato un utente.');
      }
      else{
        $.ajax({
          url: "deleteUser",
          type: "post",
          data: {
            email: table.row('.selected').data().email
          }
        })
        .done(function(data){
          if (JSON.parse(data).ok){
            table.row('.selected').remove().draw( false );
            render_info('Utente eliminato con successo.');
          }
          else{
            render_error('Problemi con la cancellazione dell\'utente');
          }
        });
      }
    });

    function reload_table($action, response, options){
      count = table.data().count();
      table.ajax.reload(function( json ){
        num_users = json.length - count;
        if( num_users > 0 ){
          if( num_users == 1 ){
            render_info('Aggiunto '+ num_users + ' utente.');
          }else{
            render_info('Aggiunti '+ num_users + ' utenti.');
          }
        }else if(num_users < 0 ){
          if( Math.abs(num_users) == 1 ){
            render_info('Rimosso '+ Math.abs(num_users) +' utente.')
          }else{
            render_info('Rimossi '+ Math.abs(num_users) +' utenti.')
          }
        }
      });
      $action.$modal.trigger('destroy.plone-modal.patterns');
    }

    new Modal($('#button-add-user'), {
      backdropOptions: {
        closeOnEsc: false,
        closeOnClick: false
      },
      actionOptions: {
        onSuccess: reload_table
      },
    });
    new Modal($('#button-import-users'), {
      backdropOptions: {
        closeOnEsc: false,
        closeOnClick: false
      },
      actionOptions: {
        onSuccess: reload_table
      },
    });

    // inizializzazione datatables
    table = $('#users-table').DataTable({
      "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.16/i18n/Italian.json"
        },
      "ajax": {
            "url": "exportUsersListAsJson",
            "dataSrc": ""
        },
      "columns": [
            { "data": "email"},
            { "data": "creation_date"},
            { "data": "is_active"}
        ]
    });

    $('#users-table tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });
  });
});
