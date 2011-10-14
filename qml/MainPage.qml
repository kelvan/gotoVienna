import QtQuick 1.1
import com.nokia.meego 1.0
import "UIConstants.js" as UIConstants
import "ExtrasConstants.js" as ExtrasConstants

Page {
    tools: commonTools

    Image {
        id: logo
        source: 'logo.png'

        anchors {
            topMargin: 25
            top: parent.top
            horizontalCenter: parent.horizontalCenter
        }
    }

    SelectionDialog {
        id: lineSelector
        titleText: 'Select line'

        model: ListModel {
            id: lineSelectorModel

            Component.onCompleted: {
                var lines = itip.get_lines()

                for (var idx in lines) {
                    lineSelectorModel.append({'name': lines[idx]})
                }
            }
        }

        // XXX It would be nice if we could make a delegate with
        // icons (i.e. U1, U2, ... in the right colors), but we
        // would have to "copy" the default delegate style

        onAccepted: {
            console.log('accepted: ' + selectedIndex)
            gline.text = lineSelectorModel.get(selectedIndex).name
        }
    }

    TextField {
        placeholderText: 'Line'

        id: gline
        anchors {
            top: logo.bottom
            left: parent.left
            topMargin: 20
            leftMargin: 10
            rightMargin: 10
            right: lineSearchButton.left
        }

        onTextChanged: {
            // TODO: Check if text matches an item in lineSelectorModel and
            // set selectedIndex in lineSelector to the right item

            if (lineSelector.selectedIndex == -1) {
                return
            }

            // Disable selection in line selector if user changes the text
            if (lineSelectorModel.get(lineSelector.selectedIndex).name != text) {
                lineSelector.selectedIndex = -1
            }
        }

         MouseArea {
             anchors.fill: parent
             drag.target: gline
             drag.axis: Drag.YAxis
             drag.minimumY: 0
             drag.maximumY: parent.height
         }
    }

    Button {
        id: lineSearchButton

        anchors {
            top: gline.top
            bottom: gline.bottom
            right: parent.right
            rightMargin: 10
        }

        width: 60
        iconSource: 'image://theme/icon-m-common-search'

        onClicked: lineSelector.open()
    }

    TextField {
        placeholderText: 'Station'
        id: gstation
        anchors {
            top: gline.bottom
            left: parent.left
            right: parent.right
            topMargin: 10
            leftMargin: 10
            rightMargin: 10
        }
    }

    ResultRealtime { id: resu }

    Button {
        id: btnSearch
        text: 'Search'
        anchors {
            top: gstation.bottom
            topMargin: 10
            horizontalCenter: parent.horizontalCenter
        }
        onClicked: {
            resu.gline = gline.text
            resu.gstation = gstation.text
            pageStack.push(resu)
            itip.search(gline.text, gstation.text)
            resu.busy = false
        }
    }
}

