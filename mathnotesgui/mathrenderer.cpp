#include "mathrenderer.h"
#include <QFile>

QString readFile (const QString& filename)
{
    QFile file(filename);
    if (file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        QTextStream stream(&file);
        return stream.readAll();
    }
    return "";
}

MathRenderer::MathRenderer(QObject *parent) : QObject(parent)
{
    view = new QWebView();

    view->setMaximumHeight(128);

    // Make webview transparent
    QPalette palette = view->palette();
    palette.setBrush(QPalette::Base, Qt::transparent);
    view->page()->setPalette(palette);
    view->setAttribute(Qt::WA_OpaquePaintEvent, false);
}

void MathRenderer::render(QString *latexString) {
//    view->setHtml(readFile(":/html/test"));
    view->setHtml(latexString);
}
