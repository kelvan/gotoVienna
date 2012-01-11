import QtQuick 1.1
import com.nokia.meego 1.0
import QtMobility.location 1.1

import "UIConstants.js" as UIConstants
import "ExtrasConstants.js" as ExtrasConstants

Page {
    tools: commonTools

    property bool canRefresh: realtimeResult.sourceUrl != '' || (realtimeResult.isStation && realtimeResult.gstation != '')
    //property alias stationSelect: stationSelector
    property variant nearbyStations

    function search() {
        lineSearchButton.clicked()
    }

    function refresh() {
        realtimeResult.refresh()
    }

    function fillNearbyStations(lat, lon) {
        nearbyStations = itip.get_nearby_stations(lat, lon)
    }

    function showNearby() {
        console.log("show nearby")

        var stations = nearbyStations
        stationSelectorModel.clear()
        for (var idx in stations) {
            stationSelectorModel.append({'name': stations[idx]})
        }

        stationSelector.open()
    }

    Text {
        visible: !parent.canRefresh
        anchors.centerIn: parent
        font.pixelSize: 30
        text: '<p><strong>Welcome, traveller!<br></strong></p><p>Press <img src="image://theme/icon-m-toolbar-search"> to search for<br>departure information.</p><p>Press <img src="image://theme/icon-m-toolbar-view-menu"> for nearby stations.<br></p><p><strong>Have a safe journey.</strong></p>'
    }

    Rectangle {
        id: header
        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
            margins: -1
        }
        border {
            color: 'black'
            width: 1
        }

        gradient: Gradient {
            GradientStop { position: 0; color: '#777' }
            GradientStop { position: 1; color: '#aaa' }
        }

        height: 80
        color: 'white'

        Image {
            id: logo
            source: 'logo.png'

            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                leftMargin: 10
            }
        }

    }

    PositionSource {
        id: positionSource
        updateInterval: 10000

        active: true

        onPositionChanged: {
            fillNearbyStations(positionSource.position.coordinate.latitude, positionSource.position.coordinate.longitude)
        }
    }

    SelectionDialog {
        id: stationSelector
        titleText: 'Select nearby station'

        model: ListModel {
            id: stationSelectorModel
        }

        onAccepted: {
            realtimeResult.isStation = true
            realtimeResult.gstation = stationSelectorModel.get(selectedIndex).name
            realtimeResult.gline = ''
            realtimeResult.sourceUrl = ''
            gline.text = ''
            gstation.text = stationSelectorModel.get(selectedIndex).name
            console.log('station to get: ' + realtimeResult.gstation)
        }
    }

    TextField {
        visible: false
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
            gstation.text = ''
        }

         MouseArea {
             anchors.fill: parent
             drag.target: gline
             drag.axis: Drag.YAxis
             drag.minimumY: 0
             drag.maximumY: parent.height
         }
    }

    LineSheet {
        id: lineSheet
        onAccepted: {
            gline.text = currentLine

            /* We usually want to select a station after selecting a line */
            stationPickerButton.clicked()
        }
    }

    Button {
        id: lineSearchButton
        visible: false

        anchors {
            top: gline.top
            bottom: gline.bottom
            right: parent.right
            rightMargin: 10
        }

        width: 60
        iconSource: 'image://theme/icon-m-common-search'

        onClicked: {
            lineSheet.currentLine = ''
            lineSheet.open()
        }
    }

    TextField {
        placeholderText: 'Station'
        id: gstation
        visible: false

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
        onAccepted: {
            gstation.text = stationSheet.currentStation

            realtimeResult.gline = stationSheet.currentLine
            realtimeResult.gstation = stationSheet.currentStation
            realtimeResult.gdirection = stationSheet.currentDirection
            realtimeResult.isStation = false

            realtimeResult.sourceUrl = itip.get_directions_url(stationSheet.currentLine, stationSheet.currentDirection, stationSheet.currentStation)
            console.log('url to get: ' + realtimeResult.sourceUrl)
            realtimeResult.refresh()

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

        visible: false

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
            top: header.bottom
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

