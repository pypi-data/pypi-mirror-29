// copyright 2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

seda = {
    toggleFormMetaVisibility: function(domid) {
        var $node = cw.jqNode(domid);
        $node.toggleClass('hidden');
        var $a = $node.parent().children('a');
        var classes = $a.attr('class').split(' ');
        var icon = classes[0];
        if (icon == 'icon-list-add') {
            classes[0] = 'icon-up-open';
        } else {
            classes[0] = 'icon-list-add';
        }
        $a.attr('class', classes.join(' '));
    },

    canMoveTo: function(moved_node, target_node, position){
        if (position === 'after' || position === 'before') {
            const target_index = target_node.parent.children.indexOf(target_node);
            if (moved_node.type === 'SEDAArchiveUnit') {
                // archive unit move
                // -> OK if before / after another archive unit
                if (target_node.type === 'SEDAArchiveUnit') {
                    return true;
                } else if (target_node.type !== 'SEDAArchiveTransfer') {
                    // -> OK if it's after the last binary/physical data object before archive unit
                    if (target_index === target_node.parent.children.length - 1
                        || target_node.parent.children[target_index + 1].type == 'SEDAArchiveUnit') {
                        return true;
                    }
                }
                return false;
            } else {
                // data object move
                // -> OK if it's after a data object of the same type
                //    or if we're moving a physical data object after the last of its kind
                return (target_node.type === moved_node.type
                       || (moved_node.type === 'SEDAPhysicalDataObject'
                           && target_node.type === 'SEDABinaryDataObject'
                           && target_node.parent.children[target_index + 1].type == 'SEDAPhysicalDataObject'));
            }
        } else {
            // special case of moving an archive unit to root: disallow if there
            // are some data objects since this is visually false, only allow
            // moving before/after existing children
            if (target_node.type === 'SEDAArchiveTransfer'
                && moved_node.type === 'SEDAArchiveUnit'
                && target_node.children[0].type != 'SEDAArchiveUnit') {
                return false;
            }
            // this is a reparenting
            // ensure the new parent target accept the moved node
            return target_node.maybeParentOf.indexOf(moved_node.type) !== -1;
        }
    }
};
