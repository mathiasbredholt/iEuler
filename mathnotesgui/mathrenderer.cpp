#include "mathrenderer.h"
#include <QFile>
#include <QDir>
#include <QWebFrame>
#include <QWebElement>
#include <QEvent>
#include <QNativeGestureEvent>

qreal MathRenderer::ZOOM_FACTOR = 1;

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
    view->setMaximumHeight(80);
    view->installEventFilter(this);
    view->setZoomFactor(MathRenderer::ZOOM_FACTOR);

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
    view->setZoomFactor(MathRenderer::ZOOM_FACTOR);
    view->page()->mainFrame()->findFirstElement("#input").setInnerXml(latexString);
    view->page()->mainFrame()->evaluateJavaScript("UpdateMath()");
}

bool MathRenderer::eventFilter(QObject *object, QEvent *e)
{
//    if (e->type() == QEvent::TouchUpdate) {

//        QNativeGestureEvent* gestureEvent =  (QNativeGestureEvent*) e;
//        //qDebug() << gestureEvent->value();
//        //qDebug() << gestureEvent->type();
//    }
    if (e->type() == QEvent::Wheel) {
        e->ignore();
        return true;
    }
    return false;
}
