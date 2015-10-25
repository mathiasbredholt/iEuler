#include "mathrenderer.h"
#include <QFile>
#include <QDir>
#include <QWebFrame>
#include <QWebElement>

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

    view->setFocusPolicy(Qt::NoFocus);

    QString html = readFile(":/webkit/test");
    QUrl baseUrl = QUrl::fromLocalFile(QDir::currentPath() + "/mathnotesgui/webkit/");
    view->setHtml(html, baseUrl);
}

void MathRenderer::render(QString latexString) {
    view->page()->mainFrame()->findFirstElement("#eq").setInnerXml("$$" + latexString + "$$");
    view->page()->mainFrame()->evaluateJavaScript(readFile(":/webkit/render"));
}
