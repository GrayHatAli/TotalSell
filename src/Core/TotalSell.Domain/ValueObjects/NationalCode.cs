namespace TotalSell.Domain.ValueObjects;

public class NationalCode : ValueObject
{
    public string Value { get; private set; } = string.Empty;

    private NationalCode() { }

    public NationalCode(string value)
    {
        if (string.IsNullOrWhiteSpace(value))
            throw new ArgumentException("National code cannot be empty", nameof(value));

        // Remove any non-digit characters
        var cleanedValue = new string(value.Where(c => char.IsDigit(c)).ToArray());
        
        if (cleanedValue.Length != 10)
            throw new ArgumentException("National code must be 10 digits", nameof(value));

        if (!IsValidNationalCode(cleanedValue))
            throw new ArgumentException("Invalid national code", nameof(value));

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

    public static implicit operator string(NationalCode nationalCode)
    {
        return nationalCode.Value;
    }

    private static bool IsValidNationalCode(string code)
    {
        if (code.Length != 10) return false;

        var sum = 0;
        for (int i = 0; i < 9; i++)
        {
            sum += int.Parse(code[i].ToString()) * (10 - i);
        }

        var remainder = sum % 11;
        var checkDigit = int.Parse(code[9].ToString());

        if (remainder < 2)
            return remainder == checkDigit;
        else
            return (11 - remainder) == checkDigit;
    }
} 