import QtQuick 1.1
import com.nokia.meego 1.0
import "UIConstants.js" as UIConstants
import "ExtrasConstants.js" as ExtrasConstants

Sheet {
    id: stationSheet
    property string currentLine: ''
    property string currentDirection: ''
    property string currentStation: ''
    property string currentUrl: ''

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
                if (selectedIndex != -1) {
                    stationSheet.currentStation = directionChooserModel.get(selectedIndex).station
                } else {
                    stationSheet.currentStation = ''
                }
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

            delegate: SheetListItem { selector: stationSelectorListView }
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
        gstation.text = stationSheet.currentStation

        realtimeResult.gline = stationSheet.currentLine
        realtimeResult.gstation = stationSheet.currentStation
        realtimeResult.gdirection = stationSheet.currentDirection
        realtimeResult.isStation = false

        realtimeResult.sourceUrl = itip.get_directions_url(stationSheet.currentLine, stationSheet.currentDirection, stationSheet.currentStation)
        console.log('url to get: ' + realtimeResult.sourceUrl)

    }
}
