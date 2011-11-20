import QtQuick 1.1
import com.nokia.meego 1.0
import QtMobility.location 1.1

PageStackWindow {
    id: appWindow

    initialPage: mainPage

    MainPage {
        id: mainPage
    }

    PositionSource {
        id: positionSource
        updateInterval: 15000

        active: !(position.longitudeValid && position.latitudeValid)
    }

    ToolBarLayout {
        id: commonTools
        visible: true
        /*ToolIcon {
            platformIconId: "toolbar-view-menu"
            anchors.right: (parent === undefined) ? undefined : parent.right
            onClicked: (menu.status == DialogStatus.Closed) ? menu.open() : menu.close()
        }*/
        ToolIcon {
              enabled: mainPage.canRefresh
              platformIconId: enabled ? 'icon-m-toolbar-refresh' : 'icon-m-toolbar-refresh-dimmed'
              anchors.right: parent.right
              onClicked: mainPage.refresh()
        }

        ToolIcon {
              platformIconId: enabled ? 'icon-m-toolbar-refresh' : 'icon-m-toolbar-refresh-dimmed'
              anchors.right: parent.right
              onClicked: mainPage.refresh()
        }

        Image {
            id: logo
            source: 'logo.png'

            anchors {
                bottomMargin: 10
                bottom: parent.bottom
                left: parent.left
                leftMargin: 10
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    //console.debug(itip.get_nearby_stations(positionSource.position.coordinate.latitude, positionSource.position.coordinate.longitude))
                    //debugText.text = itip.get_nearby_stations(positionSource.position.coordinate.latitude, positionSource.position.coordinate.longitude)
                    itip.load_nearby_departures(positionSource.position.coordinate.latitude, positionSource.position.coordinate.longitude)
                }
            }
        }

        Text {
            id: debugText
            text: ''

            anchors {
                bottomMargin: 10
                bottom: parent.bottom
                left: logo.right
                leftMargin: 10
                top: logo.top
            }
            font.pixelSize: 16
        }
    }

    /*Menu {
        id: menu
        visualParent: pageStack
        MenuLayout {
            MenuItem { text: "Test"; onClicked: pageStack.push(Qt.resolvedUrl("test.qml")) }
        }
    }*/
}
