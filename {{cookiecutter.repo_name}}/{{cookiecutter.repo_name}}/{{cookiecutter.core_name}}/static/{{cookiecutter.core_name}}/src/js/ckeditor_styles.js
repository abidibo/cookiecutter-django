CKEDITOR.dtd.$removeEmpty['i'] = false;
CKEDITOR.stylesSet.add( 'core_styles', [
    // Block-level styles.
    { name: 'Tabella responsive', element: 'div', attributes: { 'class': 'table-responsive' } },
    { name: 'Iframe responsive', element: 'div', attributes: { 'class': 'iframe-responsive' } },
    { name: 'Citazione', element: 'p', attributes: { 'class': 'blockquote' } },
    { name: 'Lista non stilizzata', element: 'ul', attributes: { 'class': 'ui list' } },
    { name: 'Segment', element: 'div', attributes: { 'class': 'ui segment' } },
    { name: 'Message', element: 'div', attributes: { 'class': 'ui message' } },
    { name: 'Warning Message', element: 'div', attributes: { 'class': 'ui warning message' } },
    { name: 'Positive Message', element: 'div', attributes: { 'class': 'ui positive message' } },
    { name: 'Negative Message', element: 'div', attributes: { 'class': 'ui negative message' } },
    { name: 'Divider', element: 'div', attributes: { 'class': 'ui divider' } },
    { name: 'H Divider', element: 'div', attributes: { 'class': 'ui horizontal divider' } },
    { name: 'Header h1', element: 'h1', attributes: { 'class': 'ui header' } },
    { name: 'Header h2', element: 'h2', attributes: { 'class': 'ui header' } },
    { name: 'Header h3', element: 'h3', attributes: { 'class': 'ui header' } },
    { name: 'Header h4', element: 'h4', attributes: { 'class': 'ui header' } },
    { name: 'Header h5', element: 'h5', attributes: { 'class': 'ui header' } },
    { name: 'Header h6', element: 'h6', attributes: { 'class': 'ui header' } },

    { name: 'Text center', element: 'div', attributes: { 'class': 'text-center' } },
    { name: 'Text center mobile', element: 'div', attributes: { 'class': 'text-center-mobile' } },

    { name: 'Table', element: 'table', attributes: { 'class': 'ui celled table' } },
    { name: 'Table striped', element: 'table', attributes: { 'class': 'ui celled striped table' } },
    { name: 'Table definition', element: 'table', attributes: { 'class': 'ui definition table' } },

    { name: 'Table row warning', element: 'tr', attributes: { 'class': 'warning' } },
    { name: 'Table row error', element: 'tr', attributes: { 'class': 'error' } },
    { name: 'Table row active', element: 'tr', attributes: { 'class': 'active' } },

    { name: 'List pdf', element: 'li', attributes: { 'class': 'ext ext-pdf' } },
    { name: 'List txt', element: 'li', attributes: { 'class': 'ext ext-txt' } },
    { name: 'List doc', element: 'li', attributes: { 'class': 'ext ext-doc' } },
    { name: 'List zip', element: 'li', attributes: { 'class': 'ext ext-zip' } },
    { name: 'List jpg', element: 'li', attributes: { 'class': 'ext ext-jpg' } },

    // Inline styles.
    { name: 'Txt evidenziato', element: 'mark', attributes: { 'class': '' } },
    { name: 'Img responsive', element: 'img', attributes: { 'class': 'img-fluid' } },
    { name: 'Img fluid', element: 'img', attributes: { 'class': 'ui fluid image' } },
    { name: 'Img bordata', element: 'img', attributes: { 'class': 'ui bordered image' } },
    { name: 'Img arrotondata', element: 'img', attributes: { 'class': 'ui rounded image' } },
    { name: 'Img circolare', element: 'img', attributes: { 'class': 'ui circular image' } },
    { name: 'Pdf icon', element: 'i', attributes: { 'class': 'file pdf icon' } },

    { name: 'Btn', element: 'a', attributes: { 'class': 'ui button' } },
    { name: 'Btn verde', element: 'a', attributes: { 'class': 'ui green button' } },
    { name: 'Btn orange', element: 'a', attributes: { 'class': 'ui orange button' } },
    { name: 'Btn red', element: 'a', attributes: { 'class': 'ui red button' } },
    { name: 'Btn custom', element: 'a', attributes: { 'class': 'ui custom small red button' } }
]);
