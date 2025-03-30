namespace TotalSell.Domain.Entities;

public class ReportCategory : BaseEntity
{
    public string Name { get; private set; }
    public string Code { get; private set; }
    public string Description { get; private set; }
    public Guid? ParentId { get; private set; }
    public ReportCategory Parent { get; private set; }
    public ICollection<ReportCategory> Children { get; private set; }
    public ICollection<Report> Reports { get; private set; }
    public bool IsActive { get; private set; }

    private ReportCategory()
    {
        Children = new List<ReportCategory>();
        Reports = new List<Report>();
    }

    public ReportCategory(
        string name,
        string code,
        string description,
        Guid? parentId = null)
    {
        Name = name;
        Code = code;
        Description = description;
        ParentId = parentId;
        Children = new List<ReportCategory>();
        Reports = new List<Report>();
        IsActive = true;
    }

    public void UpdateDetails(
        string name,
        string description)
    {
        Name = name;
        Description = description;
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