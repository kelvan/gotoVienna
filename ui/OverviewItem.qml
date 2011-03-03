import Qt 4.7

Rectangle {
    anchors.left: parent.left
    anchors.right: parent.right
    height: 70
    color: (index%2)?'#eee':'#ddd'

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
    }

    Text {
        id: time_from
        anchors.left: datum.right
        anchors.bottom: parent.verticalCenter
        text: 'von ' + modelData.time_from
        verticalAlignment: Text.AlignBottom
        width: parent.width * .2
        visible: modelData.time_from != '-'
    }

    Text {
        id: time_to
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
        anchors.fill: parent
        onClicked: parent.showDetails(modelData)
    }
}
