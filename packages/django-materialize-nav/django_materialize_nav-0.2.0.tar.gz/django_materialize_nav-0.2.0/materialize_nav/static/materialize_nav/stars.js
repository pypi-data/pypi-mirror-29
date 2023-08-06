function set_star_radio_classes(id){
    var was_checked = false;

    // Notes: icon star_class is for the aver
    jQuery(".star-item-icon", $(id).closest(".star-list")).removeClass("star_icon star_half_icon star_border_icon");
    var items = jQuery(".star-item-label", $(id).closest(".star-list"));
    for(var i=items.length-1; i >= 0 ; i--){
        was_checked = was_checked || jQuery("input:radio", items[i]).is(':checked');
        var icon = jQuery("i", items[i]);
        if(!was_checked){
            icon.addClass("star_border_icon");
        } else {
            icon.addClass("star_icon");
        }
    }
}

function set_star_ranking_classes(id){
    // Notes: icon star_class
    jQuery(".star-item-icon", $(id).closest(".star-list"))
        .removeClass("star_icon star_half_icon star_border_icon")
        .each(function(){
            $(this).addClass($(this).data("star_ranking_class"));
    });
}
