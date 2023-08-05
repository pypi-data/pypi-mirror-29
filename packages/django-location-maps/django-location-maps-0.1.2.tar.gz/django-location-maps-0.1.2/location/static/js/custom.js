String.prototype.capitalize = function(){
    return this.replace( /(^|\s)([a-z])/g , function(m,p1,p2){ return p1+p2.toUpperCase(); } );
};

String.prototype.slugify = function () {
  return this.trim().toLowerCase()
    .replace(/\s+/g, '-')
    .replace(/[^\w\-]+/g, '')
    .replace(/\-\-+/g, '-')
    .replace(/^-+/, '')
    .replace(/-+$/, '');
};

(function($){
    "use strict";

    var DjangoMap = {

        map: null,
        searchBox: null,
        marker: null,
        parserInput: {
            'route': 'address',
            'sublocality_level_1': 'neighborhood',
            'administrative_area_level_2': 'city',
            'administrative_area_level_1': 'state',
            'country': 'country',
            'postal_code': 'postal_code',
            'street_number': 'street_number'
        },

        init:function(){
            $(document).ready(function(){
                var container = $('#map');
                var zoom = 13;

                var LatLng = {
                    lat: container.data('latitude') || -22.932164,
                    lng: container.data('longitude') || -43.373225
                };

                if (container.data('latitude') !== undefined)
                    zoom = 18;

                DjangoMap.map = new google.maps.Map(
                    container.get(0),
                    {
                        center: LatLng,
                        zoom: zoom,
                        mapTypeId: 'roadmap'
                    }
                );

                if (container.data('latitude') !== undefined) {

                    DjangoMap.setMarker(LatLng.lat, LatLng.lng);
                }

                DjangoMap.initSearchBox();

                DjangoMap.map.addListener('bounds_changed', function (e) {
                    DjangoMap.searchBox.setBounds( DjangoMap.map.getBounds() );
                });

                DjangoMap.map.addListener('click', function (e) {
                    DjangoMap.setMarker(e.latLng.lat(), e.latLng.lng());
                    DjangoMap.setLocation(e.latLng);
                });
            });
        },

        initSearchBox: function(){
            var input = document.getElementById('map-input');
            this.searchBox = new google.maps.places.SearchBox( input );
            this.map.controls[ google.maps.ControlPosition.TOP_LEFT ].push( input );
            this.searchBox.addListener('places_changed', function () {
                var places = DjangoMap.searchBox.getPlaces();
                DjangoMap.setLocation(places[0].geometry.location);
                DjangoMap.setMarker(places[0].geometry.location.lat(), places[0].geometry.location.lng());
                DjangoMap.setAddress(places[0].address_components);


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

                DjangoMap.map.fitBounds(bounds);
            });
        },

        setAddress:function(Address){
            this.clearInputs();
            $.each(Address.reverse(),function(i,e){
                $.each(DjangoMap.parserInput,function(j,f){
                    if($.inArray(j,e.types) > -1){
                        var country = $('#id_country');
                        switch(f){
                            case 'country':
                                $.each(country.find('option'),function(l,g){
                                    if($(g).text().slugify() === e.long_name.slugify()) {
                                        country.val(l);
                                    }
                                });
                                break;

                            case 'state':
                                DjangoFormAjax.listStates(country.val(), e.long_name.slugify());
                                break;

                            case 'city':
                                DjangoFormAjax.listCities(country.val(), e.long_name.slugify());
                             break;

                            default:
                                $('input[name=' + f + ']').val(e.long_name);
                        }
                    }
                });
            });
        },

        clearInputs:function(){
            $.each(this.parserInput,function (i,e) {
                $('input[name=' + e + ']').val('');
            })
        },

        setLocation:function(location){
            $('input[name=latitude]').val(location.lat());
            $('input[name=longitude]').val(location.lng());
        },

        setMarker:function(lat,lng){
            if(DjangoMap.marker !== null) {
                if(typeof DjangoMap.marker.setMap === "function") {
                    DjangoMap.marker.setMap(null);
                }
            }

            this.marker = new google.maps.Marker(
                {
                    position: new google.maps.LatLng(lat,lng),
                    map: DjangoMap.map,
                    draggable:true,
                    animation: google.maps.Animation.DROP
                }
            );

            this.marker.addListener('dragend', function(e){
                DjangoMap.setLocation(e.latLng);
            });
        }
    };

    window.DjangoMap = DjangoMap;

    var DjangoFormAjax ={
        init: function (){
            this.watch();
        },

        listStates: function(country, selected){
            var states = $('#id_states');
            $(states).find('option:not([value=0])').remove();
            $.ajax({
                url:'../states/?country=' + country,
                async: false,
                success:function(data){
                    if (data.length > 0) {
                        $.each(data, function (i, e) {
                            $('#id_states').append(
                                $('<option ' + ((selected !== undefined) ? (selected === e.fields.name.slugify() ? 'selected' : '') : '') + '>')
                                    .attr('value', e.pk)
                                    .text(e.fields.name)
                            );
                        })
                    }
                }
            });
        },

        listCities: function(state, selected){
            var cities = $('#id_city');
            $(cities).find('option:not([value=0])').remove();
            $.ajax({
                url:'../cities/?state=' + state,
                async: false,
                success:function(data){
                    if(data.length > 0) {
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

        watch: function(){
            $('#id_country').on('change',function(){
                DjangoFormAjax.listStates($(this).val());
            });

            $('#id_states').on('change',function(){
                DjangoFormAjax.listCities($(this).val());
            });

        }
    };

    window.DjangoFormAjax = DjangoFormAjax;

})(jQuery);

jQuery(function ($) {
    DjangoFormAjax.init();
});