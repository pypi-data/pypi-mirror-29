String.prototype.capitalize = function () {
    return this.replace(/(^|\s)([a-z])/g, function (m, p1, p2) {
        return p1 + p2.toUpperCase();
    });
};

String.prototype.slugify = function () {
    return this.trim().toLowerCase()
        .replace(/\s+/g, '-')
        .replace(/[^\w\-]+/g, '')
        .replace(/\-\-+/g, '-')
        .replace(/^-+/, '')
        .replace(/-+$/, '');
};

$.fn.searchMap = function () {

    return this.each(function (i, e) {
        DjangoMap.initSearchBox(e, $(e).attr('id').replace('-input', ''))
    });

};
$.fn.initMap = function () {

    return this.each(function (i, e) {
        DjangoMap.initMap(e)
    });

};

(function ($) {
    "use strict";

    var DjangoMap = {

        maps: {},
        searchBox: {},
        marker: {},
        parserInput: {
            'route': 'address',
            'sublocality_level_1': 'neighborhood',
            'administrative_area_level_2': 'city',
            'administrative_area_level_1': 'state',
            'country': 'country',
            'postal_code': 'postal_code',
            'street_number': 'street_number'
        },
        init: function () {
            $(document).ready(function () {
                if ($(".map").length > 0) {
                    if($(".map").parents('[id*=_set-empty]').length > 0){
                        $(".map:not([id*='__prefix__'])").initMap();
                        $("[data-map='input']:not([id*='__prefix__'])").searchMap();

                        $('.add-row a').on('click',function(e){
                            $(".map:not([data-initialized=true]):not([id*='__prefix__'])").initMap();
                            $("[data-map='input']:not([data-initialized=true]):not([id*='__prefix__'])").searchMap();
                        });

                    }else{
                        $(".map:not([id*='__prefix__'])").initMap();
                        $("[data-map='input']:not([id*='__prefix__'])").searchMap();
                    }
                }
            });
        },

        initMap: function (element) {
            var zoom = 13;
            var map = $(element).attr('id');

            if ($(element).data('latitude') !== undefined)
                zoom = 18;

            DjangoMap.maps[map] = new google.maps.Map(
                $(element).get(0),
                {
                    center: {
                        lat: $(element).data('latitude') || -22.932164,
                        lng: $(element).data('longitude') || -43.373225
                    },
                    zoom: zoom,
                    mapTypeId: 'roadmap'
                }
            );

            if ($(element).data('latitude') !== undefined)
                DjangoMap.setMarker($(element).data('latitude'), $(element).data('longitude'), map);

            $(element).attr('data-initialized','true');
        },

        initSearchBox: function (element, map) {
            this.searchBox[map] = new google.maps.places.SearchBox(element);

            this.maps[map].controls[google.maps.ControlPosition.TOP_LEFT].push(element);

            this.searchBox[map].addListener('places_changed', function () {
                var prefix_fields = map.substring(0,map.indexOf('map'));
                var places = DjangoMap.searchBox[map].getPlaces();

                DjangoMap.setLocation(places[0].geometry.location, prefix_fields);
                DjangoMap.setMarker(places[0].geometry.location.lat(), places[0].geometry.location.lng(), map);
                DjangoMap.setAddress(places[0].address_components, prefix_fields);


                if (places.length === 0) {
                    return true;
                }

                var bounds = new google.maps.LatLngBounds();

                places.forEach(function (place) {
                    if (!place.geometry) {
                        console.log("Returned place contains no geometry");
                        return true;
                    }

                    if (place.geometry.viewport) {
                        bounds.union(place.geometry.viewport);
                    } else {
                        bounds.extend(place.geometry.location);
                    }
                });

                DjangoMap.maps[map].fitBounds(bounds);
            });

            DjangoMap.maps[map].addListener('bounds_changed', function () {
                DjangoMap.searchBox[map].setBounds(DjangoMap.maps[map].getBounds());
            });

            DjangoMap.maps[map].addListener('click', function (e) {
                DjangoMap.setMarker(e.latLng.lat(), e.latLng.lng(), map);
                DjangoMap.setLocation(e.latLng);
            });
            $(element).attr('data-initialized','true');
        },

        setAddress: function (Address, prefix) {
            this.clearInputs(prefix);
            $.each(Address.reverse(), function (i, e) {
                $.each(DjangoMap.parserInput, function (j, f) {
                    if ($.inArray(j, e.types) > -1) {
                        var country = $('#id_'+prefix+'country');
                        var states = $('#id_'+prefix+'states');
                        switch (f) {
                            case 'country':
                                $.each(country.find('option'), function (l, g) {
                                    if ($(g).text().slugify() === e.long_name.slugify()) {
                                        country.val(l);
                                    }
                                });
                                break;

                            case 'state':
                                DjangoFormAjax.listStates(country.val(), e.long_name.slugify(), prefix);
                                break;

                            case 'city':
                                DjangoFormAjax.listCities(states.val(), e.long_name.slugify(), prefix);
                                break;

                            default:
                                $('input[name=' + prefix + f + ']').val(e.long_name);
                        }
                    }
                });
            });
        },

        clearInputs: function (prefix) {
            $.each(this.parserInput, function (i, e) {
                $('input[name=' + prefix + e + ']').val('');
            })
        },

        setLocation: function (location, prefix) {
            $('input[name='+prefix+'latitude]').val(location.lat());
            $('input[name='+prefix+'longitude]').val(location.lng());
        },

        setMarker: function (lat, lng, map) {
            if (typeof DjangoMap.marker[map] === "object") {
                if (typeof DjangoMap.marker[map].setMap === "function") {
                    DjangoMap.marker[map].setMap(null);
                }
            }

            this.marker[map] = new google.maps.Marker(
                {
                    position: new google.maps.LatLng(lat, lng),
                    map: DjangoMap.maps[map],
                    draggable: true,
                    animation: google.maps.Animation.DROP
                }
            );

            this.marker[map].addListener('dragend', function (e) {
                DjangoMap.setLocation(e.latLng);
            });
        }
    };

    window.DjangoMap = DjangoMap;

    var DjangoFormAjax = {
        init: function () {
            this.watch();
        },

        listStates: function (country, selected, prefix) {
            var states = $('#id_'+prefix+'states');
            $(states).find('option:not([value=0])').remove();
            states.append(
                $('<option value="0">').text('---------------------------')
            );
            $.ajax({
                url: window.location + '../states/?country=' + country,
                async: false,
                success: function (data) {
                    if (data.length > 0) {
                        $.each(data, function (i, e) {
                            states.append(
                                $('<option ' + ((selected !== undefined) ? (selected === e.fields.name.slugify() ? 'selected' : '') : '') + '>')
                                    .attr('value', e.pk)
                                    .text(e.fields.name)
                            );
                        })
                    }
                }
            });
        },

        listCities: function (state, selected, prefix) {
            var cities = $('#id_'+prefix+'city');
            $(cities).find('option:not([value=0])').remove();
            cities.append(
                $('<option value="0">').text('---------------------------')
            );
            $.ajax({
                url: '../cities/?state=' + state,
                async: false,
                success: function (data) {
                    if (data.length > 0) {
                        $.each(data, function (i, e) {
                            $(cities).append(
                                $('<option ' + (selected !== undefined ? selected === e.fields.name.slugify() ? 'selected' : '' : '') + '>')
                                    .attr('value', e.pk)
                                    .text(e.fields.name)
                            );
                        })
                    }
                }
            });
        },

        watch: function () {
            $('[id*="country"]').on('change', function () {
                var prefix = $(this).attr('id').replace('id_', '').replace('country', '');
                DjangoFormAjax.listStates($(this).val(), undefined, prefix);
            });

            $('[id*="states"]').on('change', function () {

                var prefix = $(this).attr('id').replace('id_', '').replace('states', '');

                DjangoFormAjax.listCities($(this).val(), undefined, prefix);
            });

        }
    };

    window.DjangoFormAjax = DjangoFormAjax;

})(jQuery);

jQuery(function ($) {
    DjangoFormAjax.init();
});