namespace TotalSell.Domain.ValueObjects;

public class Address : ValueObject
{
    public string? Street { get; private set; }
    public string? City { get; private set; }
    public string? State { get; private set; }
    public string? Country { get; private set; }
    public string? PostalCode { get; private set; }

    private Address() { }

    public Address(string? street, string? city, string? state, string? country, string? postalCode)
    {
        Street = street;
        City = city;
        State = state;
        Country = country;
        PostalCode = postalCode;
    }

    protected override IEnumerable<object> GetEqualityComponents()
    {
        yield return Street ?? string.Empty;
        yield return City ?? string.Empty;
        yield return State ?? string.Empty;
        yield return Country ?? string.Empty;
        yield return PostalCode ?? string.Empty;
    }

    public override string ToString()
    {
        return $"{Street}, {City}, {State} {PostalCode}, {Country}";
    }
} 