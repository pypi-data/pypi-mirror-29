requirejs(["jquery", "mockup-patterns-modal"], function($, Modal){

  function subscribe_modal(){
    context = $('.plone-modal-body div #content-core .subscription_form').data('abs') + '/@@unsubscribe';
    if ( context ){
      portalMessage = $('.portalMessage.error');

      $('div.plone-modal-body').find( portalMessage ).each(function (){
        // trovare un metodo migliore
        if ($(portalMessage).text().search("Sei già iscritto a questa newsletter, oppure non hai ancora confermato l'iscrizione") > -1){
          var email = $('#form-widgets-email').val();
          var href = $('.redirect').attr('href')
          $('.redirect').attr('href', href + '?email=' + email)
          $('.redirect').show();
        }
      });
      $('div.plone-modal-body').find( '.portalMessage' ).each(function (){
        $('.content_container').hide()
        $('.pattern-modal-buttons').hide()
      });
    }
  }

  function render_modal(el){
    modal = new Modal($(el), {
      backdropOptions: {
        closeOnEsc: false,
        closeOnClick: false
      },
      content: '#content',
      loadLinksWithinModal: true,
      templateOptions: {
        classFooterName: 'plone-modal-footer subscribe_modal',
      }
    });
    modal.on('after-render', subscribe_modal);
  }

  // aspetto che le tile all'interno della pagina siano caricate
  $(document).ready(function(){
    if( $('.pat-tiles-management').length > 0 ){
      $('.pat-tiles-management').on('rtTilesLoaded', function(e) {
        $('#channel-subscribe a').each(function(i, el) {
            render_modal(el)
        });
      });
    }else {
      $('#channel-subscribe a').each(function(i, el) {
        render_modal(el)
      });
    }
  });
});
