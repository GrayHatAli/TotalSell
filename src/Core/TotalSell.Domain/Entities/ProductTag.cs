namespace TotalSell.Domain.Entities;

public class ProductTag : BaseEntity
{
    public Guid ProductId { get; private set; }
    public Product Product { get; private set; }
    public Guid TagId { get; private set; }
    public Tag Tag { get; private set; }

    private ProductTag() { }

    public ProductTag(Guid productId, Guid tagId)
    {
        ProductId = productId;
        TagId = tagId;
    }
} 