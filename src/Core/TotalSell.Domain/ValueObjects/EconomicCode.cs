namespace TotalSell.Domain.ValueObjects;

public class EconomicCode : ValueObject
{
    public string Value { get; private set; }

    private EconomicCode() { }

    public EconomicCode(string value)
    {
        if (string.IsNullOrWhiteSpace(value))
            throw new ArgumentException("Economic code cannot be empty", nameof(value));

        // Remove any non-digit characters
        var cleanedValue = new string(value.Where(c => char.IsDigit(c)).ToArray());
        
        if (cleanedValue.Length != 12)
            throw new ArgumentException("Economic code must be 12 digits", nameof(value));

        Value = cleanedValue;
    }

    protected override IEnumerable<object> GetEqualityComponents()
    {
        yield return Value;
    }

    public override string ToString()
    {
        return Value;
    }

    public static implicit operator string(EconomicCode economicCode)
    {
        return economicCode.Value;
    }
} 