#ifndef EULER_H
#define EULER_H

/*
    Command reference
    0: Preview
        0   cmd
        1   tab index
        2   index MSB
        3   index LSB
        [4] math string
    1: Evaluate
        0   cmd
        1   tab index
        2   index MSB
        3   index LSB
        [4] math string
    2: Open file
        0   cmd
        [1] path
    3: Save file
        0   cmd
        [1] path
    4: Render
        0   cmd
        1   tab index
        2   index MSB
        3   index LSB
        [4] latex string
    5: Load math string
        0   cmd
        1   tabIndex
        2   index MSB
        3   index LSB
        [4] math string
     6: Export pdf
        0   cmd
        [1] path
*/

#include <QObject>
#include <QDebug>
#include <QProcess>
#include <QUdpSocket>
#include <QMessageBox>

class Euler : public QObject
{
    Q_OBJECT
public:
    explicit Euler(QObject *parent = 0);
    void restartCore();
    void terminate();
    void sendMathString(int tabIndex, int index, QString mathString, bool evaluate);
    void sendOpenFileRequest(QString path);
    void sendSaveFileRequest(QString path);
    void sendExportRequest(QString path);

    static const char PREVIEW  = 0;
    static const char EVALUATE = 1;
    static const char OPEN     = 2;
    static const char SAVE     = 3;
    static const char RENDER   = 4;
    static const char MATH_STR = 5;
    static const char EXPORT   = 6;

    bool hasCrashed = false;

signals:
    void receivedLatexString(int tabIndex, int index, QString latexString);
    void receivedMathString(int tabIndex, int index, QString mathString);

public slots:

private:
    QProcess *proc;
    QUdpSocket *socket;

    void processDatagram(QByteArray datagram);

private slots:
    void readPendingDatagrams();
    void writeDatagram(QByteArray datagram);
    void readStandardOutput();
    void readStandardError();
};

#endif // EULER_H
