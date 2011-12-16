import QtQuick 1.1
import com.nokia.meego 1.0

import "UIConstants.js" as UIConstants
import "ExtrasConstants.js" as ExtrasConstants

Page {
    tools: commonTools

    property bool canRefresh: realtimeResult.sourceUrl != ''

    function refresh() {
        realtimeResult.refresh()
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

    SelectionDialog {
        id: stationSelector
        titleText: 'Select nearby station'

        model: ListModel {
            id: stationSelectorModel

            Component.onCompleted: {
                var stations = itip.get_nearby_stations(positionSource.position.coordinate.latitude, positionSource.position.coordinate.longitude)

                for (var idx in stations) {
                    stationSelectorModel.append({'name': stations[idx]})
                }
            }
        }

        // XXX It would be nice if we could make a delegate with
        // icons (i.e. U1, U2, ... in the right colors), but we
        // would have to "copy" the default delegate style

        onAccepted: {
            console.log('accepted: ' + lineSelectorModel.get(selectedIndex).name)
            //gline.text = lineSelectorModel.get(selectedIndex).name
        }
    }

    TextField {
        placeholderText: 'Line'

        id: gline
        anchors {
            top: parent.top
            left: parent.left
            topMargin: 20
            leftMargin: 10
            rightMargin: 10
            right: lineSearchButton.left
        }

        onTextChanged: {
            // TODO: Check if text matches an item in lineSelectorModel and
            // set selectedIndex in lineSelector to the right item
            gstation.text = ''

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

    /*
    LineSheet {
        id: lineSheet
    }*/

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
            right: stationPickerButton.left
            topMargin: 10
            leftMargin: 10
            rightMargin: 10*stationPickerButton.opacity
        }
    }

    StationSheet {
        id: stationSheet
    }

    Button {
        id: stationPickerButton

        anchors {
            top: gstation.top
            bottom: gstation.bottom
            right: parent.right
            rightMargin: 10
        }

        Behavior on opacity { PropertyAnimation { } }

        opacity: gline.text != '' // XXX: Check if the line is valid

        width: lineSearchButton.width * opacity
        //iconSource: 'image://theme/icon-m-common-location-picker'
        iconSource: 'image://theme/icon-m-toolbar-list'

        onClicked: {
            stationSheet.open()
            stationSheet.loadData(gline.text)
        }
    }

    ResultRealtime {
        id: realtimeResult

        anchors {
            margins: 10
            top: gstation.bottom
            left: parent.left
            bottom: parent.bottom
            right: parent.right
        }

        clip: true

        gline: stationSheet.currentLine
        gstation: stationSheet.currentStation
        gdirection: stationSheet.currentDirection

        sourceUrl: stationSheet.currentUrl
    }
}

