require.config({
    "paths": {
      "datatables": PORTAL_URL + "/++plone++rer.newsletter/scripts/datatables",
    }
});
requirejs(["jquery", "datatables"], function($, datatables){
  $(document).ready(function() {

    $('#delete-message-sent > span').on('click', function(){
      if (!(table.row('.selected').data())){
        // render error user deleted
        $('.portalMessage').removeClass('info')
                           .addClass('error')
                           .css('display', '')
                           .html('<strong>Error</strong> Prima va selezionato un messaggio.');
      }
      else{
        $.ajax({
          url: "deleteMessageFromHistory",
          type: "post",
          data: {
            message_history: table.row('.selected').data().uid
          }
        })
        .done(function(data){
          if (JSON.parse(data).ok){
            table.row('.selected').remove().draw( false );
            $('.portalMessage').removeClass('error')
                               .addClass('info')
                               .css('display', '')
                               .html('<strong>Info</strong> Storico del messaggio eliminato con successo.');
          }
          else{
            $('.portalMessage').removeClass('info')
                               .addClass('error')
                               .css('display', '')
                               .html('<strong>Error</strong> Problemi con la cancellazione dello storico del messaggio.');
          }
        });
      }
    });

    // inizializzazione datatables
    table = $('#message-table').DataTable({
      "language": {
                "url": "https://cdn.datatables.net/plug-ins/1.10.16/i18n/Italian.json"
            },
      "ajax": {
            "url": "getMessageSentDetails",
            "dataSrc": ""
        },
      "columns": [
            { "data": "uid" },
            { "data": "message"},
            { "data": "active_users"},
            { "data": "send_date"}
        ],
      "columnDefs": [
            {
                "targets": [ 0 ],
                "visible": false,
                "searchable": false
            },
        ]
    });

    $('#message-table tbody').on( 'click', 'tr', function () {
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
