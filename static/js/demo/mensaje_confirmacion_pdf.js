
// UI-Modals.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
//
// - ThemeOn.net -






function llamarMensajes	(llamada , id_certificado , empresa){

	if(  "carga_mensaje_pdf".localeCompare(llamada) == 0 ){
    // BOOTBOX - CUSTOM HTML FORM
    // =================================================================
    // Require Bootbox
    // http://bootboxjs.com/
    // =================================================================

        bootbox.dialog({
            title: empresa,
            message:'<div class="media"><div class="media-left"><div class="media-body"><p class="text-semibold text-main">Usted ha generado el certificado No  <strong class="text-primary">' + id_certificado + ' </strong></p> Para descargarlo dirijase a la bandeja de entrada de la aplicación .</div></div>',
            buttons: {
                success: {
                    label: "Aceptar",
                    className: "btn-warning",
                }
            }
        });

        $(".demo-modal-radio").niftyCheck();


    }

 }