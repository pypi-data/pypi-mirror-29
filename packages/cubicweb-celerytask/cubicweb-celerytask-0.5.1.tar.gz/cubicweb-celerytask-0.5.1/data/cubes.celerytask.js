/*
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 2.1 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.
*/

cw.celerytask = {
    autorefreshprogress: function(eid, oldState) {
        function refresh() {
            $.getJSON(BASE_URL, {eid: eid, vid: 'celerytask.jsonexport'}, function(task) {
                if (oldState === null) {
                    oldState = task.state;
                }
                var prg = document.getElementById('js-cw-celerytask-'+eid);
                if (task.progress !== null) {
                    prg.value = task.progress;
                    prg.max = task.total;
                    prg.textContent = 100 * prg.value/prg.max + ' %';
                } else {
                    prg.removeAttribute('value');
                    prg.textContent = 'unknown';
                }
                if (oldState !== task.state) {
                    var event = new CustomEvent(
                        'celerytask-statechanged',
                        {detail: {oldState: oldState, newState: task.state},
                         bubbles:true});
                    oldState = task.state;
                    prg.dispatchEvent(event);
                }
                if ((task.state != 'SUCCESS') && (task.state != 'FAILURE')) {
                    setTimeout(refresh, 3000);
                }
            });
        }
        refresh();
    },

    refresh: function(eid, elt, vid) {
        $(elt).loadxhtml(
            AJAX_BASE_URL,
            ajaxFuncArgs('view', {eid: eid, vid: vid}),
            null, 'swap');
    },

    setup: function(eid, state, vid) {
        var elt = document.getElementById('js-celerytask-'+eid);
        elt.addEventListener('celerytask-statechanged', function () {
            cw.celerytask.refresh(eid, elt, vid);
        }, false);
    },

    autorefreshprimary: function() {
        document.querySelector('body').addEventListener(
            'celerytask-statechanged', function(event) {
                if (event.detail.newState == 'SUCCESS'
                        || event.detail.newState == 'FAILURE') {
                    window.location.reload();
                }
            });
    }
};
