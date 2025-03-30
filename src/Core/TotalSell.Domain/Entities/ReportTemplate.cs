namespace TotalSell.Domain.Entities;

public class ReportTemplate : BaseEntity
{
    public Guid ReportId { get; private set; }
    public Report Report { get; private set; }
    public string Name { get; private set; }
    public string Description { get; private set; }
    public string Content { get; private set; }
    public string Format { get; private set; }
    public string Parameters { get; private set; }
    public bool IsDefault { get; private set; }
    public bool IsActive { get; private set; }

    private ReportTemplate() { }

    public ReportTemplate(
        Guid reportId,
        string name,
        string description,
        string content,
        string format,
        string parameters,
        bool isDefault = false)
    {
        ReportId = reportId;
        Name = name;
        Description = description;
        Content = content;
        Format = format;
        Parameters = parameters;
        IsDefault = isDefault;
        IsActive = true;
    }

    public void UpdateDetails(
        string name,
        string description,
        string content,
        string format,
        string parameters)
    {
        Name = name;
        Description = description;
        Content = content;
        Format = format;
        Parameters = parameters;
        UpdatedAt = DateTime.UtcNow;
    }

    public void SetAsDefault()
    {
        IsDefault = true;
        UpdatedAt = DateTime.UtcNow;
    }

    public void RemoveDefault()
    {
        IsDefault = false;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Deactivate()
    {
        IsActive = false;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Activate()
    {
        IsActive = true;
        UpdatedAt = DateTime.UtcNow;
    }
} 