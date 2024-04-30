odoo.define('material.certificate.MaterialTypeImageWidget', function (require) {
    "use strict";

    var FieldRadio = require('web.relational_fields').FieldRadio;
    var fieldRegistry = require('web.field_registry');

    var MaterialTypeImageWidget = FieldRadio.extend({
        template: 'MaterialTypeImageWidgetTemplate',
        events: _.extend({}, FieldRadio.prototype.events, {
            'click .material-type-image': '_onImageClick',
        }),

        // Extend the _render method to display images for each option
        _render: function() {
            var self = this;
            this._super.apply(this, arguments); // Call super to keep original radio button functionality intact
            
            // Ensure that the DOM is fully rendered before manipulating it
            if (this.$el) {
                var $images = this.$('.o_radio_input').map(function(index, radio) {
                    var value = $(radio).val();
                    var imageUrl = self._getImageUrl(value);
                    var $image = $('<img>', {
                        'src': imageUrl,
                        'class': 'material-type-image',
                        'data-value': value,
                        'style': 'cursor: pointer; margin-right: 10px; width: 50px; height: 50px;' // Example styling
                    });

                    // Prepend image safely after ensuring the label exists
                    $(radio).closest('label').prepend($image);
                    return $image;
                });

                // Use .append() safely, only if $images is not empty
                if ($images.length > 0) {
                    this.$el.prepend($images.toArray()); // Convert jQuery object to array for appending
                }
            }
        },

        _getImageUrl: function(value) {
            switch(value) {
                case 'pipe':
                    return 'https://cdn.karacametal.com/front/calc/ic_boru.png';
                case 'sheet':
                    return 'https://cdn.karacametal.com/front/calc/ic_sac.png';
                case 'box':
                    return 'https://cdn.karacametal.com/front/calc/ic_profil.png';
                case 'square':
                    return 'https://cdn.karacametal.com/front/calc/ic_kare.png';
                case 'bracket':
                    return 'https://cdn.karacametal.com/front/calc/ic_l.png';
                case 'flat':
                    return 'https://cdn.karacametal.com/front/calc/ic_lama.png';
                case 'billet':
                    return 'https://cdn.karacametal.com/front/calc/ic_mil.png';
                default:
                    return ''; // Default or empty image URL
            }
        },

        _onImageClick: function(event) {
            var $target = $(event.currentTarget);
            var value = $target.data('value');
            this._setValue(value);
        },
    });

    // Register the widget in the field registry
    fieldRegistry.add('material_type_image', MaterialTypeImageWidget);

    return MaterialTypeImageWidget;
});
