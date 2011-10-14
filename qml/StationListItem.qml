
import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.0

import "UIConstants.js" as UIConstants
import "ExtrasConstants.js" as ExtrasConstants

Item {
    property Item selector

    width: parent.width
    height: 60

    BorderImage {
        anchors.fill: parent
        visible: mouseArea.pressed
        source: theme.inverted ? 'image://theme/meegotouch-list-inverted-background-pressed-vertical-center': 'image://theme/meegotouch-list-background-pressed-vertical-center'
    }

    BorderImage {
        anchors.fill: parent
        visible: selector.selectedIndex == index
        source: theme.inverted ? 'image://theme/meegotouch-list-inverted-background-selected-vertical-center': 'image://theme/meegotouch-list-background-selected-vertical-center'
    }

    Item {
        anchors.fill: parent
        anchors.margins: UIConstants.DEFAULT_MARGIN

        Text {
            anchors {
                verticalCenter: parent.center
                left: parent.left
                leftMargin: 10
                right: parent.right
            }

            elide: Text.ElideRight

            text: station
            font.pixelSize: UIConstants.FONT_DEFAULT
            font.family: ExtrasConstants.FONT_FAMILY

            color: {
                if (theme.inverted) {
                    (selector.selectedIndex == index) ? UIConstants.COLOR_FOREGROUND : UIConstants.COLOR_INVERTED_FOREGROUND
                } else {
                    (selector.selectedIndex != index) ? UIConstants.COLOR_FOREGROUND : UIConstants.COLOR_INVERTED_FOREGROUND
                }
            }
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        onClicked: selector.selectedIndex = index
    }
}

