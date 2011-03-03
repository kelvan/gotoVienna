
import Qt 4.7

ListView {
    id: lv
    width: 800
    height: 400
    delegate: OverviewItem {
        onShowDetails: lv.showDetails(details)
    }

    states: [
        State {
            name: 'overview'
        },
        State {
            name: 'details'
            PropertyChanges {
                target: detailsRect
                opacity: 1
                scale: 1
            }
        }
    ]

    Rectangle {
        id: detailsRect
        width: parent.width - 50
        height: parent.height - 50
        anchors.centerIn: parent
        scale: 0
        opacity: 0
        color: '#aaa'

        border {
            color: '#888'
            width: 10
        }

        Behavior on opacity { PropertyAnimation { duration: 250 }}

        Behavior on scale {
            PropertyAnimation {
                duration: 500
                easing.type: Easing.InCubic
            }
        }

        Text {
            id: detailsTitle

            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            horizontalAlignment: Text.AlignHCenter
            anchors.topMargin: 20
            font.pixelSize: 30
        }

        MouseArea {
            anchors.fill: parent
            onClicked: lv.state = 'overview'
        }
    }

    function showDetails(details) {
        detailsTitle.text = 'FIXME - show details for ' + details.time_from
        lv.state = 'details'
    }
}

