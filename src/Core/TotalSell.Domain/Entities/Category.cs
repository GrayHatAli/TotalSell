namespace TotalSell.Domain.Entities;

public class Category : BaseEntity
{
    public string Name { get; private set; } = string.Empty;
    public string Code { get; private set; } = string.Empty;
    public string Description { get; private set; } = string.Empty;
    public Guid? ParentId { get; private set; }
    public Category? Parent { get; private set; }
    public ICollection<Category> Children { get; private set; }
    public bool IsActive { get; private set; }

    private Category()
    {
        Children = new List<Category>();
    }

    public Category(
        string name,
        string code,
        string description,
        Guid? parentId = null)
    {
        Name = name;
        Code = code;
        Description = description;
        ParentId = parentId;
        Children = new List<Category>();
        IsActive = true;
    }

    public void Update(
        string name,
        string code,
        string description)
    {
        Name = name;
        Code = code;
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