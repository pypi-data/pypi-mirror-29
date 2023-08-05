// copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
// contact http://www.logilab.fr -- mailto:contact@logilab.fr
//
// This program is free software: you can redistribute it and/or modify it under
// the terms of the GNU Lesser General Public License as published by the Free
// Software Foundation, either version 2.1 of the License, or (at your option)
// any later version.
//
// This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
// details.
//
// You should have received a copy of the GNU Lesser General Public License along
// with this program. If not, see <http://www.gnu.org/licenses/>.


jqtree = {
    jqTree: function(domid, dragAndDrop, canMoveTo) {
        var $tree = cw.jqNode(domid);

        function adjustPositionAndTarget(position, target_node, moved_node) {
            if (position === 'inside' && target_node.children.some(e => e.id === moved_node.id)) {
                position = 'before';
                target_node = target_node.children[0];
            }
            return [position, target_node];
        }

        function relativeIndex(node) {
            const children = node.parent.children;
            let result = 0;
            for (let idx=0; idx < children.length; idx++) {
                const child = children[idx];
                if (child.id === node.id) {
                    return result;
                } else if (child.type === node.type) {
                    result++;
                }
            }
        }

        // tree display and basic controls.
        $tree.tree({
            dragAndDrop: dragAndDrop,
            autoOpen: 0,  // only open level-0
            selectable: false,
            autoEscape: false,
            closedIcon: $('<i class="glyphicon glyphicon-expand"></i>'),
            openedIcon: $('<i class="glyphicon glyphicon-collapse-down"></i>'),
            onCanMove: function(node) {
                return node.maybeMoved;
            },
            onCanMoveTo: function(moved_node, target_node, position) {
                if ( target_node.id === undefined || position === 'none') {
                    return false;
                } else {
                    const args = adjustPositionAndTarget(position, target_node, moved_node);
                    position = args[0];
                    target_node = args[1];
                    return canMoveTo(moved_node, target_node, position);
                }
            },
            onCreateLi: function(node, $li) {
                $li.find('.jqtree-title').addClass(node.type);

                var selectedId = $tree.tree('getTree').children[0].selected;

                if ( selectedId !== null && node.id === selectedId ) {
                    // add "jqtreeNodeSelected" CSS class so that the current
                    // element in the tree gets highlighted.
                    $li.find('.jqtree-title').addClass('jqtreeNodeSelected');
                }
            }
        });
        // tree events bindings.
        $tree.bind(
            'tree.init',
            function() {
                var selectedId = $tree.tree('getTree').children[0].selected;
                var node = $tree.tree('getNodeById', selectedId);
                var parentNode = node.parent;
                while (parentNode !== null) {
                    $tree.tree('openNode', parentNode);
                    parentNode = parentNode.parent;
                }
            }
        );
        $tree.bind(
            'tree.move',
            function(event) {
                event.preventDefault();
                const move = event.move_info;
                function destinationIndex(position, target_node) {
                    let idx = 0;
                    if (position === 'after' && target_node.type === move.moved_node.type) {
                        idx = relativeIndex(target_node) + 1;
                    }
                    return idx;
                }

                const args = adjustPositionAndTarget(move.position, move.target_node, move.moved_node),
                      position = args[0],
                      target_node = args[1];
                if (position === 'inside') {
                    // this is a reparenting
                    asyncRemoteExec('jqtree_reparent', move.moved_node.id, target_node.id, 0);
                } else if (move.moved_node.parent !== target_node.parent) {
                    // this is a reparenting at specific index
                    asyncRemoteExec('jqtree_reparent', move.moved_node.id, target_node.parent.id,
                                    destinationIndex(position, target_node));
                } else {
                    // this is an ordering change into the same parent
                    asyncRemoteExec('jqtree_reorder', move.moved_node.parent.id, move.moved_node.id,
                                    destinationIndex(position, target_node));
                }

                // do the move after POSTing.
                move.do_move();
            }
        );
    }
};
