#ifndef CMDPANEL_H
#define CMDPANEL_H

#include <QFrame>
#include <QLineEdit>
#include <QVBoxLayout>

class CmdPanel : public QFrame
{
    Q_OBJECT
public:
    explicit CmdPanel(QWidget *parent = 0);

private:
    QLineEdit *cmdline;

signals:

public slots:

protected:
  void showEvent(QShowEvent *e);
};

#endif // CMDPANEL_H
