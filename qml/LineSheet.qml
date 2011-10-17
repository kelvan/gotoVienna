import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.0

import "UIConstants.js" as UIConstants
import "ExtrasConstants.js" as ExtrasConstants

Sheet {
    id: lineSheet
    property string currentSection: ''
    property string currentLine: ''

    acceptButtonText: 'Select'
    rejectButtonText: 'Cancel'

    function loadData() {
        var lines = itip.get_lines()

        for (var i in lines) {
            lineSelectorModel.append({'name': lines[i]})
        }
        lineSheet.currentSection = sectionName

        sectionChooserBusyIndicator.running = true

        underground.clicked()
        sectionChooser.checkedButton = underground
    }

    Connections {
        target: itip

        onLinesLoaded: {
            sectionChooserBusyIndicator.running = false

            underground.clicked()
            sectionChooser.checkedButton = underground
        }
    }

    content: Item {
        anchors.fill: parent

        ButtonRow {
            id: sectionChooser
            property string section1
            property string section2
            property string section3
            property string section4

            visible: !sectionChooserBusyIndicator.running

            function chosen(idx) {
                console.log('section chosen: '+ idx)

                lineSelectorListView.selectedIndex = -1

                if (idx == 1) {
                    lineSheet.currentSection = sectionChooser.section1
                } else if (idx == 2) {
                    lineSheet.currentSection = sectionChooser.section2
                } else if (idx == 2) {
                    lineSheet.currentSection = sectionChooser.section3
                } else {
                    lineSheet.currentSection = sectionChooser.section4
                }
                console.log(lineSheet.currentSection)

                sectionChooserModel.clear()
                var lines = itip.get_lines()

                for (var i in lines) {
                    lineSelectorModel.append({'name': lines[i]})
                }
            }

            anchors {
                margins: 10
                top: parent.top
                left: parent.left
                right: parent.right
            }

                Button {
                    id: underground
                    text: 'U-Bahn'
                    onClicked: sectionChooser.chosen(1)
                }

                Button {
                    id: tram
                    text: 'Straßenbahn'
                    onClicked: sectionChooser.chosen(2)
                }

                Button {
                    id: bus
                    text: 'Autobus'
                    onClicked: sectionChooser.chosen(3)
                }

                Button {
                    id: nightline
                    text: 'Nightline'
                    onClicked: sectionChooser.chosen(4)
                }

        }

        ListView {
            id: lineSelectorListView
            visible: !sectionChooserBusyIndicator.running

            property int selectedIndex: -1
            onSelectedIndexChanged: {
                console.log('current index: ' + selectedIndex)
                if (selectedIndex != -1) {
                    lineSheet.currentLine = sectionChooserModel.get(selectedIndex).station
                } else {
                    lineSheet.currentLine = ''
                }
            }

            anchors {
                margins: 10
                top: sectionChooserModel.bottom
                left: parent.left
                right: parent.right
                bottom: parent.bottom
            }

            clip: true

            model: ListModel {
                id: sectionChooserModel
            }

            delegate: SheetListItem { selector: lineSelectorListView }
        }

        ScrollDecorator {
            flickableItem: lineSelectorListView
        }

        BusyIndicator {
            id: sectionChooserBusyIndicator
            anchors.centerIn: parent
            visible: running
            platformStyle: BusyIndicatorStyle { size: 'large' }
        }
    }

    onAccepted: {
        gstation.text = stationSheet.currentStation

        realtimeResult.gline = stationSheet.currentLine

        realtimeResult.sourceUrl = itip.get_directions_url(lineSheet.currentLine, lineSheet.currentSection, lineSheet.currentStation)
    }
}
