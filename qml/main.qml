import QtQuick 1.1
import com.nokia.meego 1.0
import QtMobility.location 1.1

PageStackWindow {
    id: appWindow

    initialPage: mainPage
    showToolBar: aboutBox.opacity == 0

    MainPage {
        id: mainPage

        AboutBox {
            id: aboutBox
            anchors.fill: parent

            appName: aboutInfo.getAppName()
            websiteURL: aboutInfo.getWebsiteURL()
            copyright: aboutInfo.getCopyright()
            license: aboutInfo.getLicense()
            iconFilename: 'gotovienna-about-logo.png'
        }
    }

    PositionSource {
        id: positionSource
        updateInterval: 15000

        active: !(position.longitudeValid && position.latitudeValid)
    }

    ToolBarLayout {
        id: commonTools
        ToolIcon {
            platformIconId: "toolbar-view-menu"
            anchors.right: parent.right
            onClicked: menu.open()
        }

        ToolIcon {
              visible: mainPage.canRefresh
              platformIconId: 'icon-m-toolbar-refresh'
              anchors.centerIn: parent
              onClicked: mainPage.refresh()
        }

        Image {
            id: logo
            source: 'logo.png'

            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                leftMargin: 10
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

    Menu {
        id: menu

        MenuLayout {
            MenuItem {
                text: 'Nearby stations'
                onClicked: mainPage.showNearby()
            }
            MenuItem {
                text: 'About gotoVienna'
                onClicked: aboutBox.show()
            }
        }
    }
}
