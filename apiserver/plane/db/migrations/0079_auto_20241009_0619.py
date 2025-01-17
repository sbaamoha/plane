# Generated by Django 4.2.15 on 2024-10-09 06:19

from django.db import migrations


def move_attachment_to_fileasset(apps, schema_editor):
    FileAsset = apps.get_model("db", "FileAsset")
    IssueAttachment = apps.get_model("db", "IssueAttachment")

    bulk_issue_attachment = []
    for issue_attachment in IssueAttachment.objects.values(
        "issue_id",
        "project_id",
        "workspace_id",
        "asset",
        "attributes",
        "external_source",
        "external_id",
        "deleted_at",
        "created_by_id",
        "updated_by_id",
    ):
        bulk_issue_attachment.append(
            FileAsset(
                issue_id=issue_attachment["issue_id"],
                entity_type="ISSUE_ATTACHMENT",
                project_id=issue_attachment["project_id"],
                workspace_id=issue_attachment["workspace_id"],
                attributes=issue_attachment["attributes"],
                asset=issue_attachment["asset"],
                external_source=issue_attachment["external_source"],
                external_id=issue_attachment["external_id"],
                deleted_at=issue_attachment["deleted_at"],
                created_by_id=issue_attachment["created_by_id"],
                updated_by_id=issue_attachment["updated_by_id"],
                size=issue_attachment["attributes"].get("size", 0),
            )
        )

    FileAsset.objects.bulk_create(bulk_issue_attachment, batch_size=1000)


def mark_existing_file_uploads(apps, schema_editor):
    FileAsset = apps.get_model("db", "FileAsset")
    # Mark all existing file uploads as uploaded
    FileAsset.objects.update(is_uploaded=True)


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0078_fileasset_comment_fileasset_entity_type_and_more"),
    ]

    operations = [
        migrations.RunPython(
            move_attachment_to_fileasset,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.RunPython(
            mark_existing_file_uploads,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
