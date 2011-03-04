import Qt 4.7

Rectangle {
    id: row
    property color textColor: 'white'

    anchors.left: parent.left
    anchors.right: parent.right
    height: 70

    Image {
        source: 'bg.png'
        anchors.fill: parent
    }

    Rectangle {
        color: '#267'
        opacity: mouse.pressed?.4:0
        anchors.fill: parent
        Behavior on opacity { PropertyAnimation { duration: 200 } }
    }

    signal showDetails(variant details)

    Text {
        id: datum
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        verticalAlignment: Text.AlignVCenter
        text: modelData.date
        font.pixelSize: 20
        anchors.leftMargin: 30
        anchors.rightMargin: 30
        width: parent.width * .2
        color: row.textColor
    }

    Text {
        id: time_from
        color: row.textColor
        anchors.left: datum.right
        anchors.bottom: parent.verticalCenter
        text: 'von ' + modelData.time_from
        verticalAlignment: Text.AlignBottom
        width: parent.width * .2
        visible: modelData.time_from != '-'
    }

    Text {
        id: time_to
        color: row.textColor
        anchors.left: datum.right
        anchors.top: parent.verticalCenter
        text: 'bis ' + modelData.time_to
        anchors.rightMargin: 40
        verticalAlignment: Text.AlignTop
        width: time_from.width
        visible: modelData.time_to != '-'
    }

    Text {
        id: dauer
        color: row.textColor
        text: 'Dauer: ' + modelData.duration + ' (' + modelData.change + ' x umsteigen)'
        font.pixelSize: 17
        anchors.left: time_from.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        verticalAlignment: Text.AlignVCenter
        width: parent.width * .3
    }

    Text {
        id: price
        color: row.textColor
        text: 'EUR ' + modelData.price
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        verticalAlignment: Text.AlignVCenter
        width: parent.width * .1
        horizontalAlignment: Text.AlignRight
        anchors.rightMargin: 20
    }

    MouseArea {
        id: mouse
        anchors.fill: parent
        onClicked: parent.showDetails(modelData)
    }
}
