
import QtQuick 1.0

Item {
    id: settingsHeader
    property alias text: headerCaption.text
    property color color: headerCaption.visible?'#666':'#fff'

    width: parent.width
    height: headerCaption.visible?60*.7:10

    Rectangle {
        id: horizontalLine

        anchors {
            left: parent.left
            right: headerCaption.left
            rightMargin: headerCaption.visible?16:0
            verticalCenter: headerCaption.verticalCenter
        }

        height: 1
        color: settingsHeader.color
    }

    Text {
        id: headerCaption
        text: ''
        visible: text !== ''
        color: settingsHeader.color
        font.pixelSize: 17

        anchors {
            right: parent.right
            bottom: parent.bottom
        }
    }
}

