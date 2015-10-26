#include "mathrenderer.h"
#include <QFile>
#include <QDir>
#include <QWebFrame>
#include <QWebElement>
#include <QEvent>

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
    view->installEventFilter(this);
    view->setZoomFactor(1.5);

    // Make webview transparent
    QPalette palette = view->palette();
    palette.setBrush(QPalette::Base, Qt::transparent);
    view->page()->setPalette(palette);
    view->setAttribute(Qt::WA_OpaquePaintEvent, false);

    view->setFocusPolicy(Qt::NoFocus);

    QString html = readFile(":/webkit/test");
    QUrl baseUrl = QUrl::fromLocalFile(QDir::currentPath() + "/mathnotesgui/webkit/");
    view->setHtml(html, baseUrl);
//    view->page()->mainFrame()->evaluateJavaScript(readFile(":/webkit/render"));
}

void MathRenderer::render(QString latexString) {
    view->page()->mainFrame()->findFirstElement("#input").setInnerXml(latexString);
    view->page()->mainFrame()->evaluateJavaScript("UpdateMath()");
}

bool MathRenderer::eventFilter(QObject *object, QEvent *e)
{
    if (e->type() == QEvent::Wheel) e->ignore();
    return false;
}
