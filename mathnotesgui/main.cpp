#include "mainwindow.h"
#include <QApplication>
#include "util.h"
#include <QDir>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
//    QCoreApplication::setOrganizationName("QtProject");
    QCoreApplication::setApplicationName("iEuler");
//    QCoreApplication::setApplicationVersion(QT_VERSION_STR);

#ifndef QT_DEBUG
    QDir::setCurrent(qApp->applicationDirPath() + "/../../../../");
#endif
    MainWindow w;
    w.show();
    w.initRenderer();

    return app.exec();
}
