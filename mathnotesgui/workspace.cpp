#include "workspace.h"

Workspace::Workspace(QWidget *parent) : QTableWidget(parent)
{
    setFocusPolicy(Qt::ClickFocus);
    setColumnCount(2);
    setFont(parent->font());
    verticalHeader()->hide();
    horizontalHeader()->hide();
    horizontalHeader()->setStretchLastSection(true);
}

void Workspace::receivedWorkspace(int tabIndex, int index, QVariantMap workspace)
{
    int j = 0;
    QMapIterator<QString, QVariant> i(workspace);

    setRowCount(workspace.count());

    while (i.hasNext()) {
      i.next();
      setItem(j, 0, new QTableWidgetItem(i.key()));
      setItem(j, 1, new QTableWidgetItem(i.value().toString()));
      j++;
    }
}
