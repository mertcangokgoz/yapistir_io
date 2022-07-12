document.addEventListener('DOMContentLoaded', function () {

    $(document).on('click', '.notification > button.delete', function () {
        $(this).parent().addClass('is-hidden');
        return false;
    });


    let rootEl = document.documentElement;
    let $modals = getAll('.modal');
    let $modalButtons = getAll('.modal-button');
    let $modalCloses = getAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button');

    if ($modalButtons.length > 0) {
        $modalButtons.forEach(function ($el) {
            $el.addEventListener('click', function () {
                var target = $el.dataset.target;
                openModal(target);
            });
        });
    }

    if ($modalCloses.length > 0) {
        $modalCloses.forEach(function ($el) {
            $el.addEventListener('click', function () {
                closeModals();
            });
        });
    }

    function openModal(target) {
        var $target = document.getElementById(target);
        rootEl.classList.add('is-clipped');
        $target.classList.add('is-active');
    }

    function closeModals() {
        rootEl.classList.remove('is-clipped');
        $modals.forEach(function ($el) {
            $el.classList.remove('is-active');
        });
    }

    function getAll(selector) {
        return Array.prototype.slice.call(document.querySelectorAll(selector), 0);
    }


    const curLine = document.location.hash;
    if (curLine.startsWith('#L')) {
        const hashlist = curLine.substring(2).split(',');
        if (hashlist.length > 0 && hashlist[0] !== '') {
            hashlist.forEach(function (el) {
                const line = document.getElementById(`l${el}`);
                if (line) {
                    line.classList.add('marked');
                }
            });
        }
    }

    const lines = document.querySelectorAll('.snippet-code li');
    lines.forEach(function (el) {
        el.onclick = function () {
            el.classList.toggle('marked');
            let hash = 'L';
            const marked = document.querySelectorAll('.snippet-code li.marked');
            marked.forEach(function (line) {
                if (hash !== 'L') {
                    hash += ',';
                }
                hash += line.getAttribute('id').substring(1);
            });
            window.location.hash = hash;
        };
    });

    const wordwrapCheckbox = document.getElementById('wordwrap');
    const snippetDiv = document.querySelectorAll('.snippet-code');

    function toggleWordwrap() {
        if (wordwrapCheckbox.checked) {
            snippetDiv.forEach(function (i) {
                i.classList.add('wordwrap') 
                i.style="padding-right: 5px"
            });
        } else {
            snippetDiv.forEach(function (i) {
                i.classList.remove('wordwrap') 
                i.style="padding-right: 0px"
            });
        }
    }

    if (wordwrapCheckbox && snippetDiv) {
        toggleWordwrap();
        wordwrapCheckbox.onchange = toggleWordwrap;
    }

    const af = document.querySelector('.autofocus textarea');
    if (af !== null) {
        af.focus();
    }
});
