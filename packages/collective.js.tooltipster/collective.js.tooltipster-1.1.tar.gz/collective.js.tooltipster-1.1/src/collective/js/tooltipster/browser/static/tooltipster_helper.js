function tooltipster_helper(selector,
                            view_name,
                            data_parameters={},
                            theme='tooltipster-shadow',
                            animation='fade',
                            updateAnimation='fade',
                            trigger='hover') {

    jQuery(function($){

    $(selector).tooltipster({
        content: 'Loading...',
        contentAsHTML: true,
        interactive: true,
        theme: theme,
        position: 'bottom',
        animationDuration: 100,
        delay: 50,
        animation: animation,
        updateAnimation: updateAnimation,
        trigger: trigger,

        functionBefore: function (instance, helper) {
            var $origin = $(helper.origin);
            if ($origin.data('loaded') !== true) {
                // data_parameters
                parameters = {};
                for (i = 0, len = data_parameters.length; i < len; i++) {
                    value = $($origin).attr('data-'+ data_parameters[i]);
                    parameters[data_parameters[i]] = value;
                }
                // base_url
                var base_url = $($origin).attr('data-base_url');
                if (!base_url) {
                  base_url = document.baseURI;
                }
                parameters.ajax_load = new Date().getTime();

                $.ajax({
                    type: 'GET',
                    url: base_url + '/' + view_name,
                    data: parameters,
                    success: function (data) {
                        instance.content(data);
                        $origin.data('loaded', true);
                    }
                });

        }
    }
});
});
  
}