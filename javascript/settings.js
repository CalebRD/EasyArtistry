let settingsExcludeTabsFromShowAll = {
    settings_tab_defaults: 1,
    settings_tab_sysinfo: 1,
    settings_tab_actions: 1,
    settings_tab_licenses: 1,
};

function settingsShowAllTabs() {
    gradioApp().querySelectorAll('#settings > div').forEach(function(elem) {
        if (settingsExcludeTabsFromShowAll[elem.id]) return;

        elem.style.display = "block";
    });
}

onUiLoaded(function() {
    showRestoreProgressButton('txt2img', localGet("txt2img_task_id"));
    showRestoreProgressButton('img2img', localGet("img2img_task_id"));
    setupResolutionPasting('txt2img');
    setupResolutionPasting('img2img');
});

onOptionsChanged(function() {
    if (gradioApp().querySelector('#settings .settings-category')) return;

    var sectionMap = {};
    gradioApp().querySelectorAll('#settings > div > button').forEach(function(x) {
        sectionMap[x.textContent.trim()] = x;
    });

    opts._categories.forEach(function(x) {
        var section = x[0];
        var category = x[1];

        var span = document.createElement('SPAN');
        span.textContent = category;
        span.className = 'settings-category';

        var sectionElem = sectionMap[section];
        if (!sectionElem) return;

        sectionElem.parentElement.insertBefore(span, sectionElem);
    });
});
