import Qt 4.7

Rectangle {
    id: row
    property color textColor: 'white'

    anchors.left: parent.left
    anchors.right: parent.right
    height: 70

    //Image {
    //    source: 'bg.png'
    //    anchors.fill: parent
    //}

    Rectangle {
        color: '#467'
        opacity: mouse.pressed?.4:0
        anchors.fill: parent
        Behavior on opacity { PropertyAnimation { duration: 200 } }
    }

    signal showDetails(variant details)

    Text {
        id: line
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        verticalAlignment: Text.AlignVCenter
        text: modelData.date
        font.pixelSize: 20
        anchors.leftMargin: 30
        anchors.rightMargin: 30
        width: parent.width * .20
        color: row.textColor
    }

    Text {
        id: direction
        color: row.textColor
        anchors.left: line.right
        anchors.bottom: parent.verticalCenter
        text: 'dir'
        verticalAlignment: Text.AlignBottom
        width: parent.width * .40
    }

    Image {
        id: accessibility
        source: '../../wheelchair.png'
        height: 50
        width: 50
        anchors.left: direction.right
        anchors.bottom: parent.verticalCenter
    }

    Text {
        id: time
        color: row.textColor
        anchors.left: accessibility.right
        anchors.bottom: parent.verticalCenter
        text: '10 min'
        verticalAlignment: Text.AlignBottom
        width: parent.width * .20
    }

    MouseArea {
        id: mouse
        anchors.fill: parent
        onClicked: parent.showDetails(modelData)
    }
}

