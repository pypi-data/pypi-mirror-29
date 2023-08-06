
cw.search_autocomplete = function($elt, url, minlength, limit) {
    $elt.autocomplete({
        delay:10,
        minLength:minlength,
        limit:limit,
        source: function( request, response ) {
        $.getJSON(url, {
            term: extractLast( request.term ),
            all: request.term,
            facetrql: ($elt.data('facet') !== undefined) ? getCurrentRql() : ""
        }, response );
        },
        focus: function() {
            // prevent value inserted on focus
           return false;
        },
        select: function( event, ui ) {
            var terms = split( this.value );
            // remove the current input
            terms.pop();
            // add the selected item
            terms.push( ui.item.value );
            // add placeholder to get the comma-and-space at the end
            terms.push( "" );
            this.value = terms.join( " " );
            // climb up to the parent form and submit it
            var par = $elt;
            while (par.get(0).tagName != "FORM") {
                par = par.parent();
            }
            par.submit();
            return false;
        }
    });
    function split( val ) {
      return val.split( /\s+/ );
    }
    function extractLast( term ) {
      return split( term ).pop();
    }
    function getCurrentRql(){
	// XXX This should be done in an easier way...
	var divid = 'pageContent';
	var vidargs = '';
	// Get facet rql
	//jQuery(CubicWeb).trigger('facets-content-loading', [divid, '', '', vidargs]);
	var $form = $('#' + divid + 'Form');
	if ($form.length != 0){
	    var zipped = facetFormContent($form);
	    zipped[0].push('facetargs');
	    zipped[1].push(vidargs);
	    return zipped[1][zipped[0].indexOf('baserql')]}
	else {return null;}
    }
};
