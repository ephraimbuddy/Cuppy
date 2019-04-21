$(function() {
    //$('#creation_date').inputmask("9999-99-99 99:99:99");
    //bootstrap WYSIHTML5 - text editor
    $('#body').wysihtml5();

    $('.add_docs').change(function() {
        var addUrl = this[this.selectedIndex].value;
        //console.log(addUrl);
        // If the browser's back button is hit from the add interface,
        // the browser may maintain the state of the select list in the
        // list interface, in which case the previously selected option
        // will still be selected. This would mean the first option
        // (eg "Add ..."") could be selected, which contains no URL to
        // redirect to, so we guard against that, also set selectedIndex
        // back to zero, to also protect against this scenario.
        if (addUrl) {
            location.href = addUrl;
            this.selectedIndex = 0;
        }
    });
})