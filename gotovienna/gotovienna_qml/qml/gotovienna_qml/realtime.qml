import QtQuick 1.0

import Qt 4.7

Rectangle {
    width: 800
    height: 400
    color: 'black'

    property alias model: lv.model

    ListView {
        id: lv
        anchors.fill: parent

        delegate: ListItem {

        }
    }
}


