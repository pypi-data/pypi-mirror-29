$(function () {

    // Initialize autocomplete:
    //
    //
//    var allGenesArray = $.map(allGenes, function (value, key) { return { value: value, data: key }; });

    $('.autocomplete_terms').autocomplete({
        lookup: allTerms,
        minChars: 2,
        triggerSelectOnValidInput: false,
        autoSelectFirst: true,
        preventBadQueries: true,
        onSelect: function (suggestion){
            this.form.submit()
        }
    });
});
