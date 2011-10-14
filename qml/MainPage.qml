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
            right: stationPickerButton.left
            topMargin: 10
            leftMargin: 10
            rightMargin: 10*stationPickerButton.opacity
        }
        onTextChanged: {
            directionLabel.currentDirection = ''
        }
    }

    Sheet {
        id: stationSheet
        property string currentLine: ''
        property string currentDirection: ''
        property string currentStation: ''

        acceptButtonText: 'Select'
        rejectButtonText: 'Cancel'

        function loadData(lineName) {
            stationSheet.currentLine = lineName

            directionChooser.direction1 = ''
            directionChooser.direction2 = ''

            directionChooserBusyIndicator.running = true
            itip.load_directions(stationSheet.currentLine)

            firstDirection.clicked()
            directionChooser.checkedButton = firstDirection
        }

        Connections {
            target: itip

            onDirectionsLoaded: {
                directionChooserBusyIndicator.running = false

                directionChooser.direction1 = itip.get_direction(0)
                directionChooser.direction2 = itip.get_direction(1)

                firstDirection.clicked()
                directionChooser.checkedButton = firstDirection
            }
        }

        content: Item {
            anchors.fill: parent

            ButtonColumn {
                id: directionChooser
                property string direction1
                property string direction2

                visible: !directionChooserBusyIndicator.running

                function chosen(idx) {
                    console.log('direction chosen: '+ idx)

                    stationSelectorListView.selectedIndex = -1

                    if (idx == 1) {
                        stationSheet.currentDirection = directionChooser.direction1
                    } else {
                        stationSheet.currentDirection = directionChooser.direction2
                    }

                    directionChooserModel.clear()
                    var stations = itip.get_stations(stationSheet.currentLine, stationSheet.currentDirection)

                    for (var s in stations) {
                        directionChooserModel.append({'station': stations[s]})
                    }
                }

                anchors {
                    margins: 10
                    top: parent.top
                    left: parent.left
                    right: parent.right
                }

                Button {
                    id: firstDirection
                    text: 'Richtung ' + directionChooser.direction1
                    onClicked: directionChooser.chosen(1)
                }

                Button {
                    id: secondDirection
                    text: 'Richtung ' + directionChooser.direction2
                    onClicked: directionChooser.chosen(2)
                }
            }

            ListView {
                id: stationSelectorListView
                visible: !directionChooserBusyIndicator.running

                property int selectedIndex: -1
                onSelectedIndexChanged: {
                    console.log('current index: ' + selectedIndex)
                }

                anchors {
                    margins: 10
                    top: directionChooser.bottom
                    left: parent.left
                    right: parent.right
                    bottom: parent.bottom
                }

                clip: true

                model: ListModel {
                    id: directionChooserModel
                }

                delegate: StationListItem { selector: stationSelectorListView }
            }

            ScrollDecorator {
                flickableItem: stationSelectorListView
            }

            BusyIndicator {
                id: directionChooserBusyIndicator
                anchors.centerIn: parent
                visible: running
                platformStyle: BusyIndicatorStyle { size: 'large' }
            }
        }

        onAccepted: {
            if (stationSelectorListView.selectedIndex == -1) {
                gstation.text = ''
            } else {
                gstation.text = directionChooserModel.get(stationSelectorListView.selectedIndex).station
            }

            directionLabel.currentDirection = stationSheet.currentDirection
        }
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

    ResultRealtime { id: resu }

    Label {
        id: directionLabel
        property string currentDirection: ''
        text: 'Richtung ' + currentDirection

        anchors {
            left: parent.left
            right: parent.right
            top: gstation.bottom
            margins: 20*directionLabel.opacity
        }

        font.pixelSize: UIConstants.FONT_SMALL

        opacity: currentDirection != ''
        scale: opacity

        Behavior on opacity { PropertyAnimation { } }
    }

    Button {
        id: btnSearch
        text: 'Search'
        anchors {
            top: directionLabel.bottom
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

