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
        updateInterval: 10000

        onActiveChanged: {
            if (config.getGpsEnabled()) {
                positionSource.start()
            } else {
                positionSource.stop()
            }
        }

    }

    ToolBarLayout {
        id: commonTools

        ToolIcon {
            platformIconId: 'icon-m-toolbar-search'
            anchors.left: parent.left
            onClicked: mainPage.search()
        }

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

    }

    Settings{id: settings}
    MapView{id: map}

    Menu {
        id: menu

        MenuLayout {
            MenuItem {
                text: 'Nearby stations'
                onClicked: mainPage.showNearby()
            }
            MenuItem {
                text: 'Favorites'
                onClicked: mainPage.showFavorites()
            }
            //MenuItem {
            //    text: 'Map'
            //    onClicked: pageStack.push(map)
            //}
            MenuItem {
                text: 'Settings'
                onClicked: pageStack.push(settings)
            }
            MenuItem {
                text: 'About gotoVienna'
                onClicked: aboutBox.show()
            }
        }
    }
}
