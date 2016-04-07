#ifndef WORKSPACE_H
#define WORKSPACE_H

#include <QVariantList>
#include <QTableWidget>
#include <QTableWidgetItem>
#include <QHeaderView>
#include <QDebug>

#include "util.h"

class Workspace : public QTableWidget
{
    Q_OBJECT
public:
    explicit Workspace(QWidget *parent = 0);

signals:

public slots:
    void receivedWorkspace(int tabIndex, int index, QVariantMap workspace);

};

#endif // WORKSPACE_H
